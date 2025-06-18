import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
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

# --- UI ---
st.set_page_config(layout="wide")
st.title("Team Time Zone Shift Planner")
cst_start = st.slider("Client Shift Start (CST hour)", 0, 23, 9)
cst_end = st.slider("Client Shift End (CST hour)", 0, 23, 17)
if cst_end <= cst_start:
    st.error("Shift end must be after start.")
    st.stop()

st.markdown("### Adjust Start Time for Each Team Member (in CST)")

shift_data = []
for name, offset in TEAM:
    member_cst_start = st.slider(f"{name} CST Start", 0, 23, cst_start, key=name)
    member_cst_end = member_cst_start + (cst_end - cst_start)

    local_start = (datetime(2000,1,1,member_cst_start) + timedelta(hours=offset+6)).time()
    local_end = (datetime(2000,1,1,member_cst_end) + timedelta(hours=offset+6)).time()
    is_night = local_start.hour < 6 or local_end.hour > 22

    shift_data.append({
        "Name": name,
        "CST Start": member_cst_start,
        "CST End": member_cst_end,
        "Local Time": f"{local_start.strftime('%I:%M %p')} – {local_end.strftime('%I:%M %p')}",
        "Color": "#d62728" if is_night else "#1f77b4"
    })

# --- PLOTTING ---
df = pd.DataFrame(shift_data)
fig, ax = plt.subplots(figsize=(10, 6))

for i, row in df.iterrows():
    ax.barh(i, row["CST End"] - row["CST Start"], left=row["CST Start"], color=row["Color"])
    ax.text(row["CST End"] + 0.2, i, row["Local Time"], va='center', fontsize=9)

ax.set_yticks(range(len(df)))
ax.set_yticklabels(df["Name"])
ax.set_xlabel("CST Hour")
ax.set_title("Shift Timeline (CST) with Local Time Labels")
ax.set_xlim(0, 24)
ax.invert_yaxis()
plt.grid(True, axis='x')
st.pyplot(fig)

# --- OPTIONAL TABLE ---
st.markdown("### Shift Times in Local Time")
st.dataframe(df[["Name", "Local Time"]].set_index("Name"))
