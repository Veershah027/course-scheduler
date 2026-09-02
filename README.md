# Course Scheduler & Conflict Checker

A full-stack web app that lets students add their course schedule and automatically detects time conflicts between courses — built to solve a real problem I ran into registering for classes.

## Features
- Add, edit, and delete courses through a web interface
- Automatic conflict detection: checks both day and time overlap before allowing a course to be saved
- Persistent storage using a SQL database (SQLite)
- Clean, styled UI

## Tech Stack
- **Backend:** Python, Flask
- **Database:** SQLite with Flask-SQLAlchemy (ORM)
- **Frontend:** HTML, CSS, Jinja2 templating

## How Conflict Detection Works
Each course stores its days (e.g. `MWF`, `TTh`) and start/end times. When a new or edited course is submitted, the app compares it against every existing course:
1. Checks if the two courses share any day
2. If they do, checks if their time ranges overlap
3. If both are true, the save is blocked and the conflicting course is shown to the user

## Running Locally
```bash
git clone https://github.com/Veershah027/course-scheduler.git
cd course-scheduler
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
Then open `http://127.0.0.1:5000` in your browser.

## What I'd Add Next
- User accounts (multiple students, separate schedules)
- Export schedule to calendar (.ics file)
- Visual weekly calendar grid instead of a list

## Live Demo
[link here once deployed]