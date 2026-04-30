from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback_system.db'
app.config['SECRET_KEY'] = 'nsrit_feedback_secret_2024'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ===================== DATABASE MODELS =====================

class User(db.Model):
    """User model for both students and admins"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(10), nullable=False)  # 'student' or 'admin'
    name = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Student-specific fields
    branch = db.Column(db.String(50))
    semester = db.Column(db.Integer)
    roll_number = db.Column(db.String(20), unique=True)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)


class Branch(db.Model):
    """Branch/Department model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)  # CSE, ECE, etc.
    code = db.Column(db.String(10), unique=True, nullable=False)
    
    subjects = db.relationship('Subject', backref='branch', lazy=True)


class Semester(db.Model):
    """Semester model"""
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)  # 1-8
    
    subjects = db.relationship('Subject', backref='semester', lazy=True)


class Subject(db.Model):
    """Subject model with comprehensive details"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    code = db.Column(db.String(20))
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'), nullable=False)
    semester_id = db.Column(db.Integer, db.ForeignKey('semester.id'), nullable=False)
    subject_type = db.Column(db.String(30), nullable=False)  # theory, lab, elective, project, internship, mandatory
    elective_group = db.Column(db.String(50))  # e.g., 'Professional_Elective_1', 'Open_Elective_1'
    faculty_id = db.Column(db.Integer)
    mentor_id = db.Column(db.Integer)
    project_guide_id = db.Column(db.Integer)
    credits = db.Column(db.Integer, default=4)
    
    feedbacks = db.relationship('Feedback', backref='subject', lazy=True)


class Feedback(db.Model):
    """Feedback model for collecting student feedback"""
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    feedback_type = db.Column(db.String(30), nullable=False)  # subject, faculty, lab, project, internship
    rating = db.Column(db.Integer)  # 1-5 rating
    comments = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    student = db.relationship('User', backref='feedbacks')


class Complaint(db.Model):
    """Complaint model for student complaints"""
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='open')  # open, in_progress, resolved
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)
    
    student = db.relationship('User', backref='complaints')


class CollegeFeedback(db.Model):
    """College Infrastructure & Mentorship feedback"""
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    q1_rating = db.Column(db.Integer)  # Infrastructure and facilities support learning
    q1_comment = db.Column(db.Text)
    q2_rating = db.Column(db.Integer)  # Library resources and digital access
    q2_comment = db.Column(db.Text)
    q3_rating = db.Column(db.Integer)  # Mentor support
    q3_comment = db.Column(db.Text)
    q4_rating = db.Column(db.Integer)  # Co-curricular and skill development
    q4_comment = db.Column(db.Text)
    q5_rating = db.Column(db.Integer)  # Overall satisfaction
    q5_comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    student = db.relationship('User', backref='college_feedbacks')


# ===================== ACADEMIC DATA =====================
BRANCHES = [
    {'name': 'CSE', 'code': 'CSE'},
    {'name': 'CSE-AI&ML', 'code': 'CSE_AIML'},
    {'name': 'CSE-DS', 'code': 'CSE_DS'},
    {'name': 'ECE', 'code': 'ECE'},
    {'name': 'EEE', 'code': 'EEE'},
    {'name': 'Mechanical', 'code': 'MECH'},
    {'name': 'Civil', 'code': 'CIVIL'}
]

SEMESTER_1_SUBJECTS = {
    'common': [
        {'name': 'Linear Algebra and Calculus', 'type': 'theory', 'credits': 4},
        {'name': 'Engineering Physics', 'type': 'theory', 'credits': 4},
        {'name': 'Engineering Chemistry', 'type': 'theory', 'credits': 4},
        {'name': 'Basics of Civil and Mechanical Engineering', 'type': 'theory', 'credits': 3},
        {'name': 'Engineering Graphics', 'type': 'theory', 'credits': 3},
        {'name': 'Problem Solving Using C', 'type': 'theory', 'credits': 3},
        {'name': 'Physics Lab', 'type': 'lab', 'credits': 2},
        {'name': 'Chemistry Lab', 'type': 'lab', 'credits': 2},
        {'name': 'C Programming Lab', 'type': 'lab', 'credits': 2},
        {'name': 'Engineering Workshop Practice', 'type': 'lab', 'credits': 2},
    ]
}

# College Infrastructure Feedback Questions
COLLEGE_FEEDBACK_QUESTIONS = [
    {
        'id': 'q1',
        'question': 'The college infrastructure and facilities support learning',
        'description': 'Classrooms, labs, equipment, and facilities are adequate'
    },
    {
        'id': 'q2',
        'question': 'The college provides adequate library resources and digital access',
        'description': 'Books, journals, online resources, and internet access are satisfactory'
    },
    {
        'id': 'q3',
        'question': 'The college mentor/guide supports your academic and personal development',
        'description': 'Your mentor provides guidance and support for your growth'
    },
    {
        'id': 'q4',
        'question': 'The college provides opportunities for co-curricular and skill development activities',
        'description': 'Clubs, events, workshops, and training programs are available'
    },
    {
        'id': 'q5',
        'question': 'Overall, I am satisfied with the academic environment at the college',
        'description': 'General satisfaction with college infrastructure and management'
    }
]

# ===================== ROUTES =====================

@app.route('/')
def index():
    """Homepage with logo and login portals"""
    return render_template('index.html')


@app.route('/student-login', methods=['GET', 'POST'])
def student_login():
    """Student login page"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email, user_type='student').first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['user_type'] = 'student'
            session['user_name'] = user.name
            flash(f'Welcome {user.name}!', 'success')
            return redirect(url_for('student_dashboard'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('student_login.html')


@app.route('/student-register', methods=['GET', 'POST'])
def student_register():
    """Student registration page"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        roll_number = request.form.get('roll_number')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('student_register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('student_register'))
        
        user = User(
            name=name,
            email=email,
            roll_number=roll_number,
            user_type='student'
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('student_login'))
    
    return render_template('student_register.html')


@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email, user_type='admin').first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['user_type'] = 'admin'
            session['user_name'] = user.name
            flash(f'Welcome Admin {user.name}!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('admin_login.html')


@app.route('/admin-register', methods=['GET', 'POST'])
def admin_register():
    """Admin registration page"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('admin_register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('admin_register'))
        
        user = User(
            name=name,
            email=email,
            user_type='admin'
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('admin_login'))
    
    return render_template('admin_register.html')


@app.route('/student/dashboard')
def student_dashboard():
    """Student dashboard - branch and semester selection"""
    if 'user_id' not in session or session.get('user_type') != 'student':
        return redirect(url_for('student_login'))
    
    branches = Branch.query.all()
    user = User.query.get(session['user_id'])
    
    return render_template('student_dashboard.html', branches=branches, user=user)


@app.route('/student/select-branch', methods=['POST'])
def select_branch():
    """Store selected branch and semester"""
    if 'user_id' not in session:
        return redirect(url_for('student_login'))
    
    branch = request.form.get('branch')
    semester = request.form.get('semester')
    
    user = User.query.get(session['user_id'])
    user.branch = branch
    user.semester = int(semester)
    db.session.commit()
    
    session['branch'] = branch
    session['semester'] = int(semester)
    
    flash(f'Branch: {branch}, Semester: {semester} selected', 'success')
    return redirect(url_for('feedback_page'))


@app.route('/student/feedback')
def feedback_page():
    """Feedback form page"""
    if 'user_id' not in session:
        return redirect(url_for('student_login'))
    
    user = User.query.get(session['user_id'])
    
    if not user.branch or not user.semester:
        flash('Please select branch and semester first', 'warning')
        return redirect(url_for('student_dashboard'))
    
    subjects = Subject.query.filter_by(
        branch_id=db.session.query(Branch.id).filter_by(name=user.branch).scalar(),
        semester_id=user.semester
    ).all()
    
    return render_template('feedback_form.html', subjects=subjects, user=user)


@app.route('/student/submit-feedback', methods=['POST'])
def submit_feedback():
    """Submit feedback"""
    if 'user_id' not in session:
        return redirect(url_for('student_login'))
    
    subject_id = request.form.get('subject_id')
    feedback_type = request.form.get('feedback_type')
    rating = request.form.get('rating')
    comments = request.form.get('comments')
    
    feedback = Feedback(
        student_id=session['user_id'],
        subject_id=int(subject_id),
        feedback_type=feedback_type,
        rating=int(rating) if rating else None,
        comments=comments
    )
    
    db.session.add(feedback)
    db.session.commit()
    
    flash('Feedback submitted successfully!', 'success')
    return redirect(url_for('feedback_page'))


@app.route('/student/college-feedback')
def college_feedback():
    """Display college infrastructure feedback questions"""
    if 'user_id' not in session or session.get('user_type') != 'student':
        return redirect(url_for('student_login'))
    
    user = User.query.get(session['user_id'])
    
    # Check if already submitted
    existing = CollegeFeedback.query.filter_by(student_id=session['user_id']).first()
    if existing:
        flash('You have already submitted college infrastructure feedback!', 'warning')
        return redirect(url_for('student_dashboard'))
    
    return render_template('college_infrastructure.html', 
                         questions=COLLEGE_FEEDBACK_QUESTIONS,
                         user=user)


@app.route('/student/submit-college-feedback', methods=['POST'])
def submit_college_feedback():
    """Submit college infrastructure feedback"""
    if 'user_id' not in session:
        return redirect(url_for('student_login'))
    
    # Check if already submitted
    existing = CollegeFeedback.query.filter_by(student_id=session['user_id']).first()
    if existing:
        flash('You have already submitted college infrastructure feedback!', 'warning')
        return redirect(url_for('student_dashboard'))
    
    college_feedback = CollegeFeedback(
        student_id=session['user_id'],
        q1_rating=int(request.form.get('q1_rating')) if request.form.get('q1_rating') else None,
        q1_comment=request.form.get('q1_comment', ''),
        q2_rating=int(request.form.get('q2_rating')) if request.form.get('q2_rating') else None,
        q2_comment=request.form.get('q2_comment', ''),
        q3_rating=int(request.form.get('q3_rating')) if request.form.get('q3_rating') else None,
        q3_comment=request.form.get('q3_comment', ''),
        q4_rating=int(request.form.get('q4_rating')) if request.form.get('q4_rating') else None,
        q4_comment=request.form.get('q4_comment', ''),
        q5_rating=int(request.form.get('q5_rating')) if request.form.get('q5_rating') else None,
        q5_comment=request.form.get('q5_comment', ''),
    )
    
    db.session.add(college_feedback)
    db.session.commit()
    
    flash('College infrastructure feedback submitted successfully!', 'success')
    return redirect(url_for('student_dashboard'))


@app.route('/student/complaint', methods=['GET', 'POST'])
def student_complaint():
    """Student complaint submission"""
    if 'user_id' not in session:
        return redirect(url_for('student_login'))
    
    if request.method == 'POST':
        subject = request.form.get('subject')
        description = request.form.get('description')
        
        complaint = Complaint(
            student_id=session['user_id'],
            subject=subject,
            description=description
        )
        
        db.session.add(complaint)
        db.session.commit()
        
        flash('Complaint submitted successfully!', 'success')
        return redirect(url_for('student_dashboard'))
    
    return render_template('complaint_form.html')


@app.route('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard - view analytics and feedbacks"""
    if 'user_id' not in session or session.get('user_type') != 'admin':
        return redirect(url_for('admin_login'))
    
    total_feedbacks = Feedback.query.count()
    total_complaints = Complaint.query.count()
    total_students = User.query.filter_by(user_type='student').count()
    
    branches = Branch.query.all()
    
    return render_template('admin_dashboard.html', 
                         total_feedbacks=total_feedbacks,
                         total_complaints=total_complaints,
                         total_students=total_students,
                         branches=branches)


@app.route('/admin/feedbacks')
def admin_feedbacks():
    """View all feedbacks with filtering"""
    if 'user_id' not in session or session.get('user_type') != 'admin':
        return redirect(url_for('admin_login'))
    
    branch_filter = request.args.get('branch')
    semester_filter = request.args.get('semester')
    subject_filter = request.args.get('subject')
    
    query = Feedback.query
    
    if branch_filter:
        query = query.filter(Feedback.subject.has(Subject.branch.has(Branch.name == branch_filter)))
    
    if semester_filter:
        query = query.filter(Feedback.subject.has(Subject.semester_id == int(semester_filter)))
    
    if subject_filter:
        query = query.filter(Feedback.subject_id == int(subject_filter))
    
    feedbacks = query.all()
    branches = Branch.query.all()
    
    return render_template('admin_feedbacks.html', feedbacks=feedbacks, branches=branches)


@app.route('/admin/complaints')
def admin_complaints():
    """View all complaints"""
    if 'user_id' not in session or session.get('user_type') != 'admin':
        return redirect(url_for('admin_login'))
    
    status_filter = request.args.get('status', 'open')
    complaints = Complaint.query.filter_by(status=status_filter).all() if status_filter else Complaint.query.all()
    
    return render_template('admin_complaints.html', complaints=complaints)


@app.route('/admin/college-feedback')
def admin_college_feedback():
    """View all college infrastructure feedback"""
    if 'user_id' not in session or session.get('user_type') != 'admin':
        return redirect(url_for('admin_login'))
    
    college_feedbacks = CollegeFeedback.query.all()
    
    return render_template('admin_college_feedback.html', college_feedbacks=college_feedbacks)


@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))


# ===================== DATABASE INITIALIZATION =====================

def init_db():
    """Initialize database with seed data"""
    with app.app_context():
        db.create_all()
        
        # Add branches
        if Branch.query.count() == 0:
            for branch in BRANCHES:
                db.session.add(Branch(name=branch['name'], code=branch['code']))
            db.session.commit()
        
        # Add semesters
        if Semester.query.count() == 0:
            for i in range(1, 9):
                db.session.add(Semester(number=i))
            db.session.commit()
        
        # Add semester 1 subjects for all branches
        if Subject.query.filter_by(semester_id=1).count() == 0:
            semester_1 = Semester.query.filter_by(number=1).first()
            for branch in Branch.query.all():
                for subject in SEMESTER_1_SUBJECTS['common']:
                    db.session.add(Subject(
                        name=subject['name'],
                        code=f"{branch.code}_{subject['name'][:3].upper()}",
                        branch_id=branch.id,
                        semester_id=semester_1.id,
                        subject_type=subject['type'],
                        credits=subject['credits']
                    ))
            db.session.commit()
        
        # Add demo admin if not exists
        if not User.query.filter_by(email='admin@nsrit.edu', user_type='admin').first():
            admin = User(
                name='Admin',
                email='admin@nsrit.edu',
                user_type='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
