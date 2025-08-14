import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="MoveMinute - Exercise Tracker", page_icon="🏃", layout="centered")

DATA_FILE = "exercise_log.csv"
ACTIVITIES = ["Run", "Walk", "Hike", "Rock Climbing", "Badminton", "Swim", "Workout", "Other"]

# --- Helpers ---
def load_data():
    try:
        return pd.read_csv(DATA_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["date", "activity", "duration_min", "distance_miles", "notes", "timestamp"])

def save_entry(entry):
    df = load_data()
    df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

# --- Sidebar navigation ---
st.sidebar.title("🏃 MoveMinute - Exercise Tracker")
page = st.sidebar.radio("Go to", ["Log Activity", "Dashboard", "About"])

# --- Log Activity ---
if page == "Log Activity":
    st.header("Log a new activity")
    date = st.date_input("Date", value=datetime.now().date())
    activity = st.selectbox("Activity", ACTIVITIES)
    duration_min = st.number_input("Duration (minutes)", min_value=0, value=30, step=5)
    distance_miles = st.number_input("Distance (miles, optional)", min_value=0.0, step=0.1)
    notes = st.text_area("Notes (optional)")

    if st.button("Save entry"):
        if duration_min == 0 and distance_miles == 0:
            st.error("Add at least a duration or distance.")
        else:
            save_entry({
                "date": date.isoformat(),
                "activity": activity,
                "duration_min": duration_min,
                "distance_miles": distance_miles,
                "notes": notes,
                "timestamp": datetime.now().isoformat(timespec="seconds")
            })
            st.success("Entry saved!")

# --- Dashboard ---
elif page == "Dashboard":
    st.header("Activity Dashboard")
    df = load_data()
    if df.empty:
        st.info("No data yet. Log some activities!")
    else:
        st.dataframe(df)
        total_minutes = df["duration_min"].sum()
        st.metric("Total Minutes", int(total_minutes))

# --- About ---
else:
    st.header("About this app")
    st.write("""
    This simple MVP lets you log different types of physical activities and track your progress over time.
    Built for the Syrotech MVP Hackathon 2025.
    """)
