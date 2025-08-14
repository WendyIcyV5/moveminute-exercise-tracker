# MoveMinute — Multi-Activity Exercise Tracker 🏃

A tiny Streamlit app to log diverse activities (run, hike, climb, badminton, etc.), see weekly totals, track simple PRs, and stay consistent.

## ✨ Features
- Quick log: date, activity, duration, optional distance, intensity, notes
- Dashboard: last 14 days chart, activity breakdown
- Personal Records: longest session; longest run distance
- Weekly goal with progress bar
- CSV storage + export button
- High-contrast, keyboard-friendly UI

## 🛠 Tech Stack
- Python, Streamlit, pandas
- Local CSV (`exercise_log.csv`) for storage

## 🚀 Quick Start
```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
