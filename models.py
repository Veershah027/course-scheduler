from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), nullable=False)      # e.g. "CSE 205"
    title = db.Column(db.String(100), nullable=False)     # e.g. "Programming Studio"
    days = db.Column(db.String(20), nullable=False)       # e.g. "MWF" or "TTh"
    start_time = db.Column(db.String(10), nullable=False) # e.g. "09:00"
    end_time = db.Column(db.String(10), nullable=False)   # e.g. "09:50"

    def __repr__(self):
        return f"<Course {self.code}>"

def times_overlap(start1, end1, start2, end2):
    return start1 < end2 and start2 < end1

def days_overlap(days1, days2):
    # e.g. "MWF" and "TTh" share no letters, "MWF" and "MW" share M and W
    return any(day in days2 for day in split_days(days1))

def split_days(days_str):
    # Handles both "MWF" style and "TTh" style safely
    days_str = days_str.replace("Th", "R")  # Thursday -> R to avoid clashing with T (Tuesday)
    return list(days_str)

def find_conflicts(new_course, existing_courses):
    conflicts = []
    for course in existing_courses:
        if days_overlap(new_course.days, course.days):
            if times_overlap(new_course.start_time, new_course.end_time,
                              course.start_time, course.end_time):
                conflicts.append(course)
    return conflicts