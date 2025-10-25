from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime, date
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize MySQL
mysql = MySQL(app)

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first.', 'warning')
            return redirect(url_for('login'))
        
        # Verify user still exists in database
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM users WHERE id = %s", (session['user_id'],))
        user = cur.fetchone()
        cur.close()
        
        if not user:
            session.clear()
            flash('Your session has expired. Please login again.', 'warning')
            return redirect(url_for('login'))
        
        return f(*args, **kwargs)
    return decorated_function

# Home route - redirect to login or dashboard
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, username, password_hash, full_name FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['full_name'] = user['full_name']
            flash(f'Welcome back, {user["full_name"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('login.html')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        full_name = request.form['full_name']
        email = request.form.get('email', '')
        
        # Hash password
        password_hash = generate_password_hash(password)
        
        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users (username, password_hash, full_name, email) VALUES (%s, %s, %s, %s)",
                       (username, password_hash, full_name, email))
            mysql.connection.commit()
            cur.close()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash('Username already exists or registration failed.', 'danger')
    
    return render_template('register.html')

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Dashboard - main page
@app.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    cur = mysql.connection.cursor()
    
    # Get courses with detailed calculations
    cur.execute("""
        SELECT 
            c.id as course_id,
            c.course_code,
            c.course_name,
            c.total_classes,
            t.name as teacher_name,
            COALESCE(ats.required_percentage, 60.00) as required_percentage,
            COUNT(ar.id) as classes_held,
            SUM(CASE WHEN ar.status = 'present' THEN 1 ELSE 0 END) as present_count,
            SUM(CASE WHEN ar.status = 'absent' THEN 1 ELSE 0 END) as absent_count
        FROM courses c
        JOIN teachers t ON c.teacher_id = t.id
        JOIN enrollments e ON c.id = e.course_id
        LEFT JOIN attendance_records ar ON e.id = ar.enrollment_id
        LEFT JOIN attendance_settings ats ON c.id = ats.course_id AND ats.user_id = %s
        WHERE e.user_id = %s
        GROUP BY c.id, c.course_code, c.course_name, c.total_classes, t.name, ats.required_percentage
        ORDER BY c.course_code
    """, (user_id, user_id))
    courses_data = cur.fetchall()
    cur.close()
    
    # Calculate smart metrics for each course
    courses = []
    for course in courses_data:
        total_classes = course['total_classes']
        classes_held = course['classes_held'] or 0
        present = course['present_count'] or 0
        absent = course['absent_count'] or 0
        required_percentage = course['required_percentage']
        
        # Calculate percentage based on TOTAL classes (not just held)
        attendance_percentage = (present / total_classes * 100) if total_classes > 0 else 0
        
        # Calculate predictions
        required_present = (required_percentage * total_classes) / 100
        classes_needed = max(0, int(required_present - present) + (1 if required_present - present > int(required_present - present) else 0))
        
        # Calculate classes can miss
        # If we need more present classes, we can only miss: remaining - classes_needed
        # If we already have enough, we can miss all remaining
        remaining_classes = max(0, total_classes - classes_held)
        if classes_needed > 0:
            classes_can_miss = max(0, remaining_classes - classes_needed)
        else:
            classes_can_miss = remaining_classes
        
        # Determine zone status
        danger_zone = (remaining_classes > 0 and remaining_classes == classes_needed)
        dead_zone = (present + remaining_classes) < required_present
        
        # Add to course dict
        course_dict = dict(course)
        course_dict['attendance_percentage'] = round(attendance_percentage, 2)
        course_dict['classes_can_miss'] = classes_can_miss
        course_dict['danger_zone'] = danger_zone
        course_dict['dead_zone'] = dead_zone
        course_dict['remaining_classes'] = remaining_classes
        
        courses.append(course_dict)
    
    return render_template('dashboard.html', courses=courses)

# Course details page
@app.route('/course/<int:course_id>')
@login_required
def course_detail(course_id):
    user_id = session['user_id']
    cur = mysql.connection.cursor()
    
    # Get course info and enrollment
    cur.execute("""
        SELECT c.*, t.name as teacher_name, e.id as enrollment_id
        FROM courses c
        JOIN teachers t ON c.teacher_id = t.id
        JOIN enrollments e ON c.id = e.course_id
        WHERE c.id = %s AND e.user_id = %s
    """, (course_id, user_id))
    course = cur.fetchone()
    
    if not course:
        flash('Course not found.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Get attendance records
    cur.execute("""
        SELECT * FROM attendance_records
        WHERE enrollment_id = %s
        ORDER BY class_date DESC
    """, (course['enrollment_id'],))
    attendance = cur.fetchall()
    
    # Get attendance settings
    cur.execute("""
        SELECT required_percentage FROM attendance_settings
        WHERE user_id = %s AND course_id = %s
    """, (user_id, course_id))
    settings = cur.fetchone()
    required_percentage = settings['required_percentage'] if settings else 60.0
    
    # Calculate statistics based on total_classes from course
    total_classes = course['total_classes']
    classes_held = len(attendance)  # Classes marked so far
    present = sum(1 for a in attendance if a['status'] == 'present')
    absent = classes_held - present
    
    # Current percentage based on TOTAL classes (not held classes)
    current_percentage = (present / total_classes * 100) if total_classes > 0 else 0
    
    # Calculate classes needed to reach target
    # Formula: need P such that (present + P) / (total_classes) >= required_percentage / 100
    # Solving: P >= (required_percentage * total_classes / 100) - present
    required_present = (required_percentage * total_classes) / 100
    classes_needed = max(0, int(required_present - present) + (1 if required_present - present > int(required_present - present) else 0))
    
    # Remaining classes
    remaining_classes = max(0, total_classes - classes_held)
    
    # Calculate classes user can miss
    # If we need more present classes, we can only miss: remaining - classes_needed
    # If we already have enough, we can miss all remaining
    if classes_needed > 0:
        classes_can_miss = max(0, remaining_classes - classes_needed)
    else:
        classes_can_miss = remaining_classes
    
    # Danger Zone: Cannot miss any more classes
    # This happens when: remaining_classes == classes_needed
    danger_zone = (remaining_classes > 0 and remaining_classes == classes_needed)
    
    # Dead Zone: Even attending all remaining classes won't help
    # This happens when: present + remaining_classes < required_present
    dead_zone = (present + remaining_classes) < required_present
    
    cur.close()
    
    return render_template('course_detail.html', 
                         course=course, 
                         attendance=attendance,
                         total_classes=total_classes,
                         classes_held=classes_held,
                         remaining_classes=remaining_classes,
                         present=present,
                         absent=absent,
                         current_percentage=round(current_percentage, 2),
                         required_percentage=required_percentage,
                         classes_needed=classes_needed,
                         classes_can_miss=classes_can_miss,
                         danger_zone=danger_zone,
                         dead_zone=dead_zone)


# Mark attendance
@app.route('/course/<int:course_id>/mark', methods=['GET', 'POST'])
@login_required
def mark_attendance(course_id):
    user_id = session['user_id']
    
    if request.method == 'POST':
        class_date = request.form['class_date']
        status = request.form['status']
        notes = request.form.get('notes', '')
        
        cur = mysql.connection.cursor()
        
        # Get enrollment_id and course details
        cur.execute("""
            SELECT e.id as enrollment_id, c.total_classes
            FROM enrollments e
            JOIN courses c ON e.course_id = c.id
            WHERE e.user_id = %s AND e.course_id = %s
        """, (user_id, course_id))
        result = cur.fetchone()
        
        if result:
            enrollment_id = result['enrollment_id']
            total_classes = result['total_classes']
            
            # Check current attendance count
            cur.execute("""
                SELECT COUNT(*) as count FROM attendance_records
                WHERE enrollment_id = %s
            """, (enrollment_id,))
            count_result = cur.fetchone()
            classes_held = count_result['count'] if count_result else 0
            
            # Validate against total_classes
            if classes_held >= total_classes:
                flash(f'Cannot add more attendance! Already marked {classes_held} out of {total_classes} total classes.', 'danger')
                cur.close()
                return redirect(url_for('course_detail', course_id=course_id))
            
            try:
                cur.execute("""
                    INSERT INTO attendance_records (enrollment_id, class_date, status, notes)
                    VALUES (%s, %s, %s, %s)
                """, (enrollment_id, class_date, status, notes))
                mysql.connection.commit()
                flash('Attendance marked successfully!', 'success')
            except Exception as e:
                flash(f'Error marking attendance: {str(e)}', 'danger')
        else:
            flash('Enrollment not found!', 'danger')
        
        cur.close()
        return redirect(url_for('course_detail', course_id=course_id))
    
    # GET request
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT c.*, COUNT(ar.id) as classes_held
        FROM courses c
        LEFT JOIN enrollments e ON c.id = e.course_id AND e.user_id = %s
        LEFT JOIN attendance_records ar ON e.id = ar.enrollment_id
        WHERE c.id = %s
        GROUP BY c.id
    """, (user_id, course_id))
    course = cur.fetchone()
    cur.close()
    
    return render_template('mark_attendance.html', course=course, course_id=course_id)

# Quick mark attendance (from dashboard)
@app.route('/course/<int:course_id>/quick-mark/<status>', methods=['POST'])
@login_required
def quick_mark_attendance(course_id, status):
    user_id = session['user_id']
    
    # Validate status
    if status not in ['present', 'absent']:
        flash('Invalid status!', 'danger')
        return redirect(url_for('dashboard'))
    
    cur = mysql.connection.cursor()
    
    # Get enrollment_id and course details
    cur.execute("""
        SELECT e.id as enrollment_id, c.total_classes
        FROM enrollments e
        JOIN courses c ON e.course_id = c.id
        WHERE e.user_id = %s AND e.course_id = %s
    """, (user_id, course_id))
    result = cur.fetchone()
    
    if result:
        enrollment_id = result['enrollment_id']
        total_classes = result['total_classes']
        
        # Check current attendance count
        cur.execute("""
            SELECT COUNT(*) as count FROM attendance_records
            WHERE enrollment_id = %s
        """, (enrollment_id,))
        count_result = cur.fetchone()
        classes_held = count_result['count'] if count_result else 0
        
        # Validate against total_classes
        if classes_held >= total_classes:
            flash(f'Cannot add more attendance! Already marked {classes_held} out of {total_classes} total classes.', 'danger')
            cur.close()
            return redirect(url_for('dashboard'))
        
        # Use today's date
        from datetime import date
        today = date.today()
        
        try:
            cur.execute("""
                INSERT INTO attendance_records (enrollment_id, class_date, status, notes)
                VALUES (%s, %s, %s, %s)
            """, (enrollment_id, today, status, 'Quick marked from dashboard'))
            mysql.connection.commit()
            flash(f'Attendance marked as {status.upper()} for today!', 'success')
        except Exception as e:
            flash(f'Error marking attendance: {str(e)}', 'danger')
    else:
        flash('Enrollment not found!', 'danger')
    
    cur.close()
    return redirect(url_for('dashboard'))

# Update attendance
@app.route('/attendance/<int:attendance_id>/edit', methods=['POST'])
@login_required
def edit_attendance(attendance_id):
    status = request.form['status']
    notes = request.form.get('notes', '')
    
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE attendance_records 
        SET status = %s, notes = %s
        WHERE id = %s
    """, (status, notes, attendance_id))
    mysql.connection.commit()
    cur.close()
    
    flash('Attendance updated successfully!', 'success')
    return redirect(request.referrer or url_for('dashboard'))

# Delete attendance record
@app.route('/attendance/<int:attendance_id>/delete', methods=['POST'])
@login_required
def delete_attendance(attendance_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM attendance_records WHERE id = %s", (attendance_id,))
    mysql.connection.commit()
    cur.close()
    
    flash('Attendance record deleted successfully!', 'success')
    return redirect(request.referrer or url_for('dashboard'))

# Manage courses (view user's own courses)
@app.route('/courses')
@login_required
def courses():
    user_id = session['user_id']
    cur = mysql.connection.cursor()
    
    # Get user's own courses with teacher info and enrollment status
    cur.execute("""
        SELECT c.*, t.name as teacher_name,
        EXISTS(SELECT 1 FROM enrollments WHERE user_id = %s AND course_id = c.id) as is_enrolled
        FROM courses c
        JOIN teachers t ON c.teacher_id = t.id
        WHERE c.user_id = %s
        ORDER BY c.course_code
    """, (user_id, user_id))
    all_courses = cur.fetchall()
    cur.close()
    
    return render_template('courses.html', courses=all_courses)

# Add new course
@app.route('/course/add', methods=['GET', 'POST'])
@login_required
def add_course():
    user_id = session['user_id']
    
    if request.method == 'POST':
        course_code = request.form['course_code']
        course_name = request.form['course_name']
        teacher_id = request.form['teacher_id']
        semester = request.form.get('semester', '')
        total_classes = request.form.get('total_classes', 0)
        required_percentage = request.form.get('required_percentage', 60.00)
        
        cur = mysql.connection.cursor()
        try:
            # Insert course
            cur.execute("""
                INSERT INTO courses (user_id, course_code, course_name, teacher_id, semester, total_classes)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (user_id, course_code, course_name, teacher_id, semester, total_classes))
            course_id = cur.lastrowid
            
            # Auto-enroll user in their own course
            cur.execute("INSERT INTO enrollments (user_id, course_id) VALUES (%s, %s)", (user_id, course_id))
            
            # Create attendance setting with user-specified percentage
            cur.execute("""
                INSERT INTO attendance_settings (user_id, course_id, required_percentage)
                VALUES (%s, %s, %s)
            """, (user_id, course_id, required_percentage))
            
            mysql.connection.commit()
            flash('Course added successfully!', 'success')
            return redirect(url_for('courses'))
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Failed to add course. Course code might already exist. Error: {str(e)}', 'danger')
        finally:
            cur.close()
    
    # GET request - show form with teachers list
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM teachers WHERE user_id = %s ORDER BY name", (user_id,))
    teachers = cur.fetchall()
    cur.close()
    
    return render_template('add_course.html', teachers=teachers)

# Add new teacher
@app.route('/teacher/add', methods=['GET', 'POST'])
@login_required
def add_teacher():
    user_id = session['user_id']
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form.get('email', '')
        department = request.form.get('department', '')
        
        cur = mysql.connection.cursor()
        try:
            cur.execute("""
                INSERT INTO teachers (user_id, name, email, department)
                VALUES (%s, %s, %s, %s)
            """, (user_id, name, email, department))
            mysql.connection.commit()
            flash('Teacher added successfully!', 'success')
            
            # Redirect back to add course if that's where we came from
            if request.args.get('redirect') == 'add_course':
                return redirect(url_for('add_course'))
            return redirect(url_for('teachers'))
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Failed to add teacher. Error: {str(e)}', 'danger')
        finally:
            cur.close()
    
    return render_template('add_teacher.html')

# View all teachers
@app.route('/teachers')
@login_required
def teachers():
    user_id = session['user_id']
    cur = mysql.connection.cursor()
    
    cur.execute("""
        SELECT t.*, COUNT(c.id) as course_count
        FROM teachers t
        LEFT JOIN courses c ON t.id = c.teacher_id AND c.user_id = %s
        WHERE t.user_id = %s
        GROUP BY t.id
        ORDER BY t.name
    """, (user_id, user_id))
    teachers_list = cur.fetchall()
    cur.close()
    
    return render_template('teachers.html', teachers=teachers_list)

# Edit teacher
@app.route('/teacher/<int:teacher_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_teacher(teacher_id):
    user_id = session['user_id']
    cur = mysql.connection.cursor()
    
    # Check if teacher belongs to user
    cur.execute("SELECT * FROM teachers WHERE id = %s AND user_id = %s", (teacher_id, user_id))
    teacher = cur.fetchone()
    
    if not teacher:
        flash('Teacher not found or you do not have permission to edit.', 'danger')
        cur.close()
        return redirect(url_for('teachers'))
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form.get('email', '')
        department = request.form.get('department', '')
        
        try:
            cur.execute("""
                UPDATE teachers 
                SET name = %s, email = %s, department = %s
                WHERE id = %s AND user_id = %s
            """, (name, email, department, teacher_id, user_id))
            mysql.connection.commit()
            flash('Teacher updated successfully!', 'success')
            cur.close()
            return redirect(url_for('teachers'))
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Failed to update teacher. Error: {str(e)}', 'danger')
    
    cur.close()
    return render_template('edit_teacher.html', teacher=teacher)

# Delete teacher
@app.route('/teacher/<int:teacher_id>/delete', methods=['POST'])
@login_required
def delete_teacher(teacher_id):
    user_id = session['user_id']
    
    cur = mysql.connection.cursor()
    # Check if teacher belongs to user
    cur.execute("SELECT id FROM teachers WHERE id = %s AND user_id = %s", (teacher_id, user_id))
    teacher = cur.fetchone()
    
    if teacher:
        # Check if teacher has courses
        cur.execute("SELECT COUNT(*) as count FROM courses WHERE teacher_id = %s AND user_id = %s", (teacher_id, user_id))
        result = cur.fetchone()
        
        if result['count'] > 0:
            flash('Cannot delete teacher who has courses assigned.', 'danger')
        else:
            cur.execute("DELETE FROM teachers WHERE id = %s", (teacher_id,))
            mysql.connection.commit()
            flash('Teacher deleted successfully!', 'success')
    else:
        flash('Teacher not found.', 'danger')
    
    cur.close()
    return redirect(url_for('teachers'))

# Delete course
# Edit course
@app.route('/course/<int:course_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_course(course_id):
    user_id = session['user_id']
    cur = mysql.connection.cursor()
    
    # Check if course belongs to user
    cur.execute("SELECT * FROM courses WHERE id = %s AND user_id = %s", (course_id, user_id))
    course = cur.fetchone()
    
    if not course:
        flash('Course not found or you do not have permission to edit it.', 'danger')
        cur.close()
        return redirect(url_for('courses'))
    
    # Get current required percentage
    cur.execute("""
        SELECT required_percentage FROM attendance_settings
        WHERE user_id = %s AND course_id = %s
    """, (user_id, course_id))
    settings = cur.fetchone()
    required_percentage = settings['required_percentage'] if settings else 60.0
    
    if request.method == 'POST':
        course_code = request.form['course_code']
        course_name = request.form['course_name']
        teacher_id = request.form['teacher_id']
        semester = request.form.get('semester', '')
        total_classes = request.form.get('total_classes', 0)
        new_required_percentage = request.form.get('required_percentage', required_percentage)
        
        try:
            # Update course details
            cur.execute("""
                UPDATE courses 
                SET course_code = %s, course_name = %s, teacher_id = %s, 
                    semester = %s, total_classes = %s
                WHERE id = %s AND user_id = %s
            """, (course_code, course_name, teacher_id, semester, total_classes, course_id, user_id))
            
            # Update or insert attendance settings
            cur.execute("""
                INSERT INTO attendance_settings (user_id, course_id, required_percentage)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE required_percentage = %s
            """, (user_id, course_id, new_required_percentage, new_required_percentage))
            
            mysql.connection.commit()
            flash('Course updated successfully!', 'success')
            cur.close()
            return redirect(url_for('courses'))
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Failed to update course. Error: {str(e)}', 'danger')
    
    # GET request - show form with current course data and teachers list
    cur.execute("SELECT * FROM teachers WHERE user_id = %s ORDER BY name", (user_id,))
    teachers = cur.fetchall()
    cur.close()
    
    return render_template('edit_course.html', course=course, teachers=teachers, required_percentage=required_percentage)

# Delete course
@app.route('/course/<int:course_id>/delete', methods=['POST'])
@login_required
def delete_course(course_id):
    user_id = session['user_id']
    
    cur = mysql.connection.cursor()
    # Check if course belongs to user
    cur.execute("SELECT id FROM courses WHERE id = %s AND user_id = %s", (course_id, user_id))
    course = cur.fetchone()
    
    if course:
        cur.execute("DELETE FROM courses WHERE id = %s", (course_id,))
        mysql.connection.commit()
        flash('Course deleted successfully!', 'success')
    else:
        flash('Course not found or you do not have permission to delete it.', 'danger')
    
    cur.close()
    return redirect(url_for('courses'))

# Enroll in a course (auto-enrolled when creating, this is for re-enrollment)
@app.route('/course/<int:course_id>/enroll', methods=['POST'])
@login_required
def enroll_course(course_id):
    user_id = session['user_id']
    
    cur = mysql.connection.cursor()
    # Verify course belongs to user
    cur.execute("SELECT id FROM courses WHERE id = %s AND user_id = %s", (course_id, user_id))
    course = cur.fetchone()
    
    if not course:
        flash('Course not found.', 'danger')
        cur.close()
        return redirect(url_for('courses'))
    
    try:
        cur.execute("INSERT INTO enrollments (user_id, course_id) VALUES (%s, %s)", (user_id, course_id))
        # Create default attendance setting
        cur.execute("""
            INSERT INTO attendance_settings (user_id, course_id, required_percentage)
            VALUES (%s, %s, 60.00)
        """, (user_id, course_id))
        mysql.connection.commit()
        flash('Successfully enrolled in course!', 'success')
    except Exception as e:
        flash('Already enrolled or enrollment failed.', 'danger')
    cur.close()
    
    return redirect(url_for('courses'))

# Unenroll from a course (DEPRECATED - removed, use delete instead)
# @app.route('/course/<int:course_id>/unenroll', methods=['POST'])
# @login_required
# def unenroll_course(course_id):
#     user_id = session['user_id']
#     
#     cur = mysql.connection.cursor()
#     cur.execute("DELETE FROM enrollments WHERE user_id = %s AND course_id = %s", (user_id, course_id))
#     mysql.connection.commit()
#     cur.close()
#     
#     flash('Successfully unenrolled from course!', 'success')
#     return redirect(url_for('courses'))

# Update required attendance percentage (DEPRECATED - now handled in edit_course)
# @app.route('/course/<int:course_id>/settings', methods=['POST'])
# @login_required
# def update_settings(course_id):
#     user_id = session['user_id']
#     required_percentage = float(request.form['required_percentage'])
#     
#     if required_percentage < 0 or required_percentage > 100:
#         flash('Percentage must be between 0 and 100.', 'danger')
#         return redirect(url_for('course_detail', course_id=course_id))
#     
#     cur = mysql.connection.cursor()
#     cur.execute("""
#         INSERT INTO attendance_settings (user_id, course_id, required_percentage)
#         VALUES (%s, %s, %s)
#         ON DUPLICATE KEY UPDATE required_percentage = %s
#     """, (user_id, course_id, required_percentage, required_percentage))
#     mysql.connection.commit()
#     cur.close()
#     
#     flash(f'Required attendance percentage updated to {required_percentage}%!', 'success')
#     return redirect(url_for('course_detail', course_id=course_id))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
