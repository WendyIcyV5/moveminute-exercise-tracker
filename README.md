# MoveMinute — Multi-Activity Exercise Tracker 🏃

A simple and private Streamlit app to log all kinds of physical activities — from running and hiking to rock climbing, badminton, swimming, and more.  
Stay consistent, track your progress, and keep your data to yourself.

## ✨ Features
- **Quick logging**: Date, activity type, duration (minutes), optional distance, and personal notes
- **Dashboard**: activity chart & breakdown
- **Personal records**: total minutes in the last 7 days & total running distance in the last 30 days
- **Offline-friendly**: Local CSV storage with export option
- **Accessible UI**: High-contrast design & keyboard-friendly navigation

## 🛠 Tech Stack
- **Backend/UI**: Python + Streamlit
- **Data handling**: pandas
- **Storage**: Local CSV file (`exercise_log.csv`)

## 🚀 Quick Start
```bash
# Clone the repository
git clone https://github.com/WendyIcyV5/moveminute-exercise-tracker.git
cd moveminute-exercise-tracker

# Create and activate virtual environment
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

# Install dependencies and run
pip install -r requirements.txt
streamlit run app.py
