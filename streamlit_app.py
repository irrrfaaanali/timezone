import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# --- CONFIG ---
TEAM = [
    ("Hady (Egypt)", 2),
    ("Awais (Pakistan)", 5),
    ("Umar (India)", 5.5),
    ("Sahil (India)", 5.5),
    ("Mushahid (India)", 5.5),
    ("Irfan (India)", 5.5),
    ("Vaibhav (India)", 5.5),
    ("Timothy (Philippines)", 8),
    ("Roman (Ukraine)", 3),
]

# --- UI: Select Client Time Window ---
st.title("Team Time Zone Shift Planner")
st.subheader("Adjust each team member's CST shift start time")

cst_start_hour = st.slider("Client Shift Start (CST)", 0, 23, 9)
cst_end_hour = st.slider("Client Shift End (CST)", 0, 23, 17)

if cst_end_hour <= cst_start_hour:
    st.error("End time must be after start time")
    st.stop()

# --- Team Schedule Sliders ---
st.markdown("---")
st.markdown("### Adjust Shifts (CST hours)")
shift_data = []
for name, offset in TEAM:
    shift_cst = st.slider(f"{name} CST Start", 0, 23, cst_start_hour, key=name)
    start_cst = datetime(2000, 1, 1, shift_cst)
    end_cst = datetime(2000, 1, 1, shift_cst + (cst_end_hour - cst_start_hour))
    start_local = start_cst + timedelta(hours=offset + 6)
    end_local = end_cst + timedelta(hours=offset + 6)

    is_night = start_local.hour < 6 or end_local.hour > 22
    shift_data.append({
        "Name": name,
        "Local Start": start_local.time(),
        "Local End": end_local.time(),
        "CST Start": shift_cst,
        "CST End": shift_cst + (cst_end_hour - cst_start_hour),
        "Night Shift": is_night
    })

# --- Chart ---
df = pd.DataFrame(shift_data)
df["Shift"] = df.apply(lambda r: f"{r['Local Start']} – {r['Local End']}", axis=1)
fig = px.timeline(
    df,
    x_start="CST Start",
    x_end="CST End",
    y="Name",
    color="Night Shift",
    labels={"Night Shift": "Night Shift"},
    title="Shift Blocks (Based on CST input, local time shown)"
)
fig.update_layout(xaxis_title="CST Hour", yaxis_title="Team Member", showlegend=False)
st.plotly_chart(fig, use_container_width=True)

# --- Table ---
st.markdown("### Shift Details")
st.dataframe(df[["Name", "Shift"]].set_index("Name"))
