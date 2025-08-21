import streamlit as st
import pandas as pd
from datetime import datetime

# set up the page configuration
st.set_page_config(page_title="MoveMinute - Exercise Tracker", page_icon="🏃", layout="centered")

DATA_FILE = "exercise_log.csv"
ACTIVITIES = ["Gym run", "Outdoor run", "Hike", "Rock Climbing", "Badminton", "Other"]

# --- Helpers ---
def load_data():
    """Load the exercise log data from CSV, or create an empty DataFrame if it doesn't exist."""
    try:
        return pd.read_csv(DATA_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["date", "activity", "duration_min", "distance_miles", "notes"])

def save_entry(entry):
    """Save a new activity entry to the CSV file."""
    df = load_data()
    df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

def get_activity_options():
    opts = list(ACTIVITIES)
    df = load_data()
    if not df.empty and "activity" in df:
        for act in df["activity"].dropna().tolist():
            if act not in opts and act != "Other":
                opts.insert(-1, act)  # put before "Other"
    return opts

# --- Sidebar navigation ---
st.sidebar.title("🏃 MoveMinute - Exercise Tracker")
page = st.sidebar.radio("Go to", ["Log Activity", "Dashboard", "About"])

# --- Log Activity ---
if page == "Log Activity":
    st.header("Log a new activity")

    date = st.date_input("Date", value=datetime.now().date())

    activity_options = get_activity_options()
    activity_choice = st.selectbox("Activity", activity_options)

    custom_activity = None
    if activity_choice == "Other":
        custom_activity = st.text_input("Type your activity", placeholder="e.g. Walk, Swim")

    duration_min = st.number_input("Duration (minutes)", min_value=0, value=30, step=5)
    distance_miles = st.text_input("Distance (miles, optional)")
    if distance_miles.strip() == "":
        distance_miles = None
    else:
        try:
            distance_miles = float(distance_miles)
        except ValueError:
            st.error("Please enter a number for distance.")
            distance_miles = None

    notes = st.text_area("Notes (optional)")

    # Final activity to save
    final_activity = (custom_activity.strip().title() if custom_activity else activity_choice)

    if st.button("Save entry"):
        if activity_choice == "Other" and not custom_activity:
            st.error("Please type the activity name for 'Other'.")
        elif duration_min == 0 and distance_miles == 0:
            st.error("Add at least a duration or distance.")
        else:
            save_entry({
                "date": date.isoformat(),
                "activity": final_activity,
                "duration_min": duration_min,
                "distance_miles": distance_miles,
                "notes": notes
            })
            st.success(f"Entry saved for {final_activity}!")

# --- Dashboard ---
elif page == "Dashboard":
    st.header("Activity Dashboard")
    df = load_data()
    if df.empty:
        st.info("No data yet. Log some activities!")
    else:
        # Parse & sort dates
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.sort_values("date", ascending=False)

        # Display metrics (keep your existing ones here)
        today = datetime.now().date()
        seven_days_ago = today - pd.Timedelta(days=7)
        recent_df = df[df["date"].dt.date >= seven_days_ago]
        total_minutes = pd.to_numeric(recent_df["duration_min"], errors="coerce").fillna(0).sum()
        st.metric("Total Minutes (last 7 days)", int(total_minutes))

        # Pretty display (no truncation on Notes; column widths controlled)
        df_display = df.copy()
        # Keep date as datetime for DateColumn; show as YYYY-MM-DD
        # Ensure numeric columns are numeric for NumberColumn
        df_display["duration_min"] = pd.to_numeric(df_display["duration_min"], errors="coerce")
        df_display["distance_miles"] = pd.to_numeric(df_display.get("distance_miles", 0), errors="coerce")

        # --- Last 30 days running distance (Gym run + Outdoor run combined) ---
        today = datetime.now().date()
        month_ago = today - pd.Timedelta(days=30)

        month_df = df[df["date"].dt.date >= month_ago].copy()
        month_df["distance_miles"] = pd.to_numeric(month_df.get("distance_miles", 0), errors="coerce").fillna(0)

        # Case-insensitive match on activity names
        acts = month_df["activity"].astype(str).str.strip().str.lower()
        running_mask = acts.isin({"gym run", "outdoor run"})

        running_distance_30d = month_df.loc[running_mask, "distance_miles"].sum()

        st.metric("Running Distance (last 30d)", f"{running_distance_30d:.2f} mi")


        st.data_editor(
            df_display,
            hide_index=True,
            use_container_width=True,
            disabled=True,  # read-only table
            column_order=["date", "activity", "duration_min", "distance_miles", "notes"],
            column_config={
                "date": st.column_config.DateColumn(
                    "Date",
                    format="YYYY-MM-DD"
                ),
                "activity": st.column_config.TextColumn("Activity"),
                "duration_min": st.column_config.NumberColumn(
                    "Duration (min)",
                    step=5
                ),
                "distance_miles": st.column_config.NumberColumn(
                    "Distance (mi)",
                    step=0.1,
                    format="%.2f"
                ),
                "notes": st.column_config.TextColumn(
                    "Notes",
                    width="large"  # "small" | "medium" | "large"
                    # (Text will wrap within the column.)
                ),
            },
        )

# --- About ---
else:
    st.header("About this app")
    st.write("""
    This simple MVP lets you log different types of physical activities and track your progress over time.  
    Built for the Syrotech MVP Hackathon 2025.
    """)
