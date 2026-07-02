import streamlit as st
from datetime import datetime, timedelta
import pytz

# Set up page styling and title
st.set_page_config(page_title="Double Out Rest Calculator", page_icon="✈️", layout="centered")

st.title("✈️ Double Out Rest Calculator")
st.write("Calculate your required Part 121 rest windows and tracking targets on the go.")

st.markdown("---")

# 1. User Inputs
st.subheader("📋 Flight Leg Details")

col1, col2 = st.columns(2)
with col1:
   block_hours = st.number_input("Total Block Time (Hours)", min_value=0.0, max_value=150.0, value=0, step=0.1, help="Enter total block hours for the flight or sequence.")
with col2:
    # Default to HKT
    tz_choice = st.selectbox("Arrival Local Timezone", [
        "HKT (Hong Kong)", 
        "Alaska (AKST/AKDT)", 
        "Pacific (PST/PDT)",
        "Hawaii (HST)",
        "Central (CST/CDT)", 
        "Eastern (EST/EDT)"
    ])

# Timezone mapping
tz_map = {
    "HKT (Hong Kong)": "Asia/Hong_Kong",
    "Alaska (AKST/AKDT)": "America/Anchorage",
    "Pacific (PST/PDT)": "America/Los_Angeles",
    "Hawaii (HST)": "Pacific/Honolulu",
    "Central (CST/CDT)": "America/Chicago",
    "Eastern (EST/EDT)": "America/New_York"
}
chosen_tz = pytz.timezone(tz_map[tz_choice])

col3, col4 = st.columns(2)
with col3:
    arrival_date = st.date_input("Arrival Date (Local)", value=datetime.now(chosen_tz).date())
with col4:
    arrival_time = st.time_input("Arrival Time (Local)", value=datetime.now(chosen_tz).time())

st.markdown("---")

# 2. Calculation Logic
if st.button("🚀 Calculate Rest Windows", use_container_width=True):
    # Combine input date and time into a localized datetime object
    local_arrival_dt = chosen_tz.localize(datetime.combine(arrival_date, arrival_time))
    
    # Convert arrival to Zulu
    zulu_arrival_dt = local_arrival_dt.astimezone(pytz.utc)
    
    # Double Out Math (Block * 2)
    required_rest_hours = block_hours * 2
    
    # Calculate when rest ends
    rest_ends_zulu = zulu_arrival_dt + timedelta(hours=required_rest_hours)
    rest_ends_local = rest_ends_zulu.astimezone(chosen_tz)
    
    # 3. Web UI Display Results
    st.subheader("📊 Legality Summary")
    
    # Metrics display
    m_col1, m_col2 = st.columns(2)
    m_col1.metric(label="Total Block Checked", value=f"{block_hours:.1f} hrs")
    m_col2.metric(label="Required Rest Window", value=f"{required_rest_hours:.1f} hrs")
    
    st.markdown("#### 🛬 Arrival References")
    st.info(f"**Zulu:** {zulu_arrival_dt.strftime('%H:%M Z (%b %d)')}  \n"
            f"**Local:** {local_arrival_dt.strftime('%H:%M')} {local_arrival_dt.strftime('%Z (%b %d)')}")
    
    st.markdown("#### 🔓 Double Out Ends (Legal to Fly)")
    st.success(f"**Zulu:** {rest_ends_zulu.strftime('%H:%M Z (%b %d)')}  \n"
               f"**Local:** {rest_ends_local.strftime('%H:%M')} {rest_ends_local.strftime('%Z (%b %d)')}")
