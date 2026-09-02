from flask import Flask, render_template, request, redirect, url_for
from models import db, Course, find_conflicts

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scheduler.db'
db.init_app(app)

@app.route('/')
def home():
    courses = Course.query.all()
    return render_template('home.html', courses=courses)

@app.route('/add', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        new_course = Course(
            code=request.form['code'],
            title=request.form['title'],
            days=request.form['days'],
            start_time=request.form['start_time'],
            end_time=request.form['end_time']
        )
        existing_courses = Course.query.all()
        conflicts = find_conflicts(new_course, existing_courses)

        if conflicts:
            conflict_names = ", ".join(f"{c.code} ({c.days} {c.start_time}-{c.end_time})" for c in conflicts)
            return render_template('add_course.html', error=f"Conflict with: {conflict_names}")

        db.session.add(new_course)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_course.html')

@app.route('/delete/<int:course_id>')
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/edit/<int:course_id>', methods=['GET', 'POST'])
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)

    if request.method == 'POST':
        updated = Course(
            code=request.form['code'],
            title=request.form['title'],
            days=request.form['days'],
            start_time=request.form['start_time'],
            end_time=request.form['end_time']
        )
        other_courses = Course.query.filter(Course.id != course_id).all()
        conflicts = find_conflicts(updated, other_courses)

        if conflicts:
            conflict_names = ", ".join(f"{c.code} ({c.days} {c.start_time}-{c.end_time})" for c in conflicts)
            return render_template('edit_course.html', course=course, error=f"Conflict with: {conflict_names}")

        course.code = request.form['code']
        course.title = request.form['title']
        course.days = request.form['days']
        course.start_time = request.form['start_time']
        course.end_time = request.form['end_time']
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('edit_course.html', course=course)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)