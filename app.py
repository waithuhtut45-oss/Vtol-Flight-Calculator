import streamlit as st
import math
st.set_page_config(page_title="Complete VTOL Flight Calculator", page_icon="🛩️")
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="collapsedControl"] {visibility: visible !important;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.set_page_config(page_title="Complete VTOL Flight Calculator", page_icon="🛩️")
st.title("🛩️ VTOL Drone Flight Distance & Duration Calculator")

st.sidebar.header("1. ဖြောင့်တန်းသော လမ်းကြောင်း (Cruise)")
outward_dist = st.sidebar.number_input("အသွား ဖြောင့်တန်းသည့် အကွာအဝေး (km):", value=15.0)
return_dist = st.sidebar.number_input("အပြန် ဖြောင့်တန်းသည့် အကွာအဝေး (km):", value=15.0)
target_altitude = st.sidebar.number_input("ရောက်ရှိလိုသည့် ပစ်မှတ်အမြင့် (Target Altitude in meters):", value=1000.0)

st.sidebar.header("2. အမြင့်တက်စဉ် အဝိုင်းပတ်ခြင်း (Climbing Spiral)")
climb_turns = st.sidebar.number_input("တက်စဉ် အဝိုင်းပတ် အရေအတွက် (Climb Turns):", value=3, step=1)
climb_radius = st.sidebar.number_input("တက်စဉ် ကွေ့ဝိုင်းအချင်းဝက် - Radius (meters):", value=50.0)

st.sidebar.header("3. အမြင့်ဆင်းစဉ် အဝိုင်းပတ်ခြင်း (Descending Spiral)")
desc_turns = st.sidebar.number_input("ဆင်းစဉ် အဝိုင်းပတ် အရေအတွက် (Descent Turns):", value=3, step=1)
desc_radius = st.sidebar.number_input("ဆင်းစဉ် ကွေ့ဝိုင်းအချင်းဝက် - Radius (meters):", value=50.0)

st.sidebar.header("4. ပျံသန်းမှု မြန်နှုန်း (Airspeed)")
airspeed_mps = st.sidebar.number_input("လေယာဉ်အမြန်နှုန်း (Airspeed in m/s):", value=22.0)

if st.button("Calculate Complete Flight & Duration"):
    target_alt_km = target_altitude / 1000.0
    
    # 1. တက်စဉ် အဝိုင်းပတ် (Climbing Spiral) တွက်ချက်ခြင်း
    if climb_turns > 0:
        climb_circumference = 2 * math.pi * climb_radius  # meters
        alt_gain_per_turn_km = (target_altitude / climb_turns) / 1000.0
        climb_circ_km = climb_circumference / 1000.0
        spiral_climb_per_turn = math.sqrt((climb_circ_km * climb_circ_km) + (alt_gain_per_turn_km * alt_gain_per_turn_km))
        total_climb_spiral = spiral_climb_per_turn * climb_turns
    else:
        total_climb_spiral = 0.0

    # 2. ဆင်းစဉ် အဝိုင်းပတ် (Descending Spiral) တွက်ချက်ခြင်း
    if desc_turns > 0:
        desc_circumference = 2 * math.pi * desc_radius  # meters
        alt_drop_per_turn_km = (target_altitude / desc_turns) / 1000.0
        desc_circ_km = desc_circumference / 1000.0
        spiral_desc_per_turn = math.sqrt((desc_circ_km * desc_circ_km) + (alt_drop_per_turn_km * alt_drop_per_turn_km))
        total_desc_spiral = spiral_desc_per_turn * desc_turns
    else:
        total_desc_spiral = 0.0

    # 3. ဖြောင့်တန်းသော လမ်းကြောင်းများ (Outward & Return Cruise with Altitude)
    outward_base = math.sqrt((outward_dist * outward_dist) + (target_alt_km * target_alt_km))
    return_base = math.sqrt((return_dist * return_dist) + (target_alt_km * target_alt_km))
    
    # 4. စုစုပေါင်း အကွာအဝေး (Grand Total in km)
    grand_total_km = outward_base + return_base + total_climb_spiral + total_desc_spiral
    
    # 5. ကြာချိန် တွက်ချက်ခြင်း (Duration Calculation)
    # အကွာအဝေး (km) ကို မီတာပြောင်းရန် 1000 နဲ့ မြှောက်ပါ၊ ပြီးလျှင် m/s ဖြင့် စားပါ (စက္ကန့်ထွက်မည်)
    total_distance_meters = grand_total_km * 1000.0
    if airspeed_mps > 0:
        total_duration_seconds = total_distance_meters / airspeed_mps
    else:
        total_duration_seconds = 0.0
        
    # စက္ကန့်ကို မိနစ်နှင့် နာရီသို့ ပြောင်းလဲခြင်း
    hours = int(total_duration_seconds // 3600)
    minutes = int((total_duration_seconds % 3600) // 60)
    seconds = int(total_duration_seconds % 60)

    # ရလဒ်များ ပြသခြင်း
    st.success("--- လေကြောင်းပျံသန်းမှု အသေးစိတ် ရလဒ်များ ---")
    st.write(f"📈 တက်စဉ် အဝိုင်းပတ် စုစုပေါင်းအကွာအဝေး: {total_climb_spiral:.2f} km")
    st.write(f"📉 ဆင်းစဉ် အဝိုင်းပတ် စုစုပေါင်းအကွာအဝေး: {total_desc_spiral:.2f} km")
    st.write(f"🔹 အသွား ဖြောင့်တန်းသော လမ်းကြောင်း: {outward_base:.2f} km")
    st.write(f"🔹 အပြန် ဖြောင့်တန်းသော လမ်းကြောင်း: {return_base:.2f} km")
    st.markdown("---")
    st.markdown(f"### 🎯 စုစုပေါင်း ပျံသန်းရမည့် အကွာအဝေး: {grand_total_km:.2f} km")
    st.markdown(f"⏱️ စုစုပေါင်း ကြာချိန် (Flight Duration): {hours} နာရီ ၊ {minutes} မိနစ် ၊ {seconds} စက္ကန့် ({total_duration_seconds:.1f} စက္ကန့်)")
