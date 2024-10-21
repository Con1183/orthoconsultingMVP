from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, PasswordField, DateField
from wtforms.validators import DataRequired, Email, Optional, EqualTo
from sqlalchemy.exc import IntegrityError
import datetime
from functools import wraps
import os
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '1202')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orthodontic.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    assessments = db.relationship('Assessment', backref='patient', lazy=True)

class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.date.today)
    facial_symmetry = db.Column(db.String(100))
    profile_type = db.Column(db.String(100))
    lip_competence = db.Column(db.String(100))
    profile_notes = db.Column(db.Text)
    breathing_pattern = db.Column(db.String(100))
    swallowing_pattern = db.Column(db.String(100))
    speech_issues = db.Column(db.String(100))
    functional_notes = db.Column(db.Text)
    pain = db.Column(db.String(100))
    clicking = db.Column(db.String(100))
    range_of_motion = db.Column(db.String(100))
    tmj_notes = db.Column(db.Text)
    teeth_condition = db.Column(db.String(100))
    gum_health = db.Column(db.String(100))
    occlusion = db.Column(db.String(100))
    intra_oral_notes = db.Column(db.Text)
    diagnosis = db.Column(db.Text)
    treatment_objectives = db.Column(db.Text)
    proposed_treatment = db.Column(db.Text)
    estimated_duration = db.Column(db.String(100))
    treatment_notes = db.Column(db.Text)

# Forms
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class PatientForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[Optional()])
    submit = SubmitField('Add Patient')

class PatientAssessmentForm(FlaskForm):
    facial_symmetry = SelectField('Facial Symmetry', choices=[('', 'Select an option'), ('Symmetrical', 'Symmetrical'), ('Asymmetrical', 'Asymmetrical')], validators=[Optional()])
    profile_type = SelectField('Profile Type', choices=[('', 'Select an option'), ('Convex', 'Convex'), ('Concave', 'Concave'), ('Straight', 'Straight')], validators=[Optional()])
    lip_competence = SelectField('Lip Competence', choices=[('', 'Select an option'), ('Competent', 'Competent'), ('Incompetent', 'Incompetent')], validators=[Optional()])
    profile_notes = TextAreaField('Profile Notes', validators=[Optional()])
    breathing_pattern = SelectField('Breathing Pattern', choices=[('', 'Select an option'), ('Nasal', 'Nasal'), ('Mouth', 'Mouth'), ('Mixed', 'Mixed')], validators=[Optional()])
    swallowing_pattern = SelectField('Swallowing Pattern', choices=[('', 'Select an option'), ('Normal', 'Normal'), ('Tongue Thrust', 'Tongue Thrust')], validators=[Optional()])
    speech_issues = StringField('Speech Issues', validators=[Optional()])
    functional_notes = TextAreaField('Functional Notes', validators=[Optional()])
    pain = SelectField('Pain', choices=[('', 'Select an option'), ('None', 'None'), ('Mild', 'Mild'), ('Moderate', 'Moderate'), ('Severe', 'Severe')], validators=[Optional()])
    clicking = SelectField('Clicking', choices=[('', 'Select an option'), ('None', 'None'), ('Occasional', 'Occasional'), ('Frequent', 'Frequent')], validators=[Optional()])
    range_of_motion = SelectField('Range of Motion', choices=[('', 'Select an option'), ('Normal', 'Normal'), ('Limited', 'Limited')], validators=[Optional()])
    tmj_notes = TextAreaField('TMJ Notes', validators=[Optional()])
    teeth_condition = StringField('Teeth Condition', validators=[Optional()])
    gum_health = SelectField('Gum Health', choices=[('', 'Select an option'), ('Healthy', 'Healthy'), ('Gingivitis', 'Gingivitis'), ('Periodontitis', 'Periodontitis')], validators=[Optional()])
    occlusion = StringField('Occlusion', validators=[Optional()])
    intra_oral_notes = TextAreaField('Intra-Oral Notes', validators=[Optional()])
    diagnosis = TextAreaField('Diagnosis', validators=[Optional()])
    treatment_objectives = TextAreaField('Treatment Objectives', validators=[Optional()])
    proposed_treatment = TextAreaField('Proposed Treatment', validators=[Optional()])
    estimated_duration = StringField('Estimated Duration', validators=[Optional()])
    treatment_notes = TextAreaField('Treatment Notes', validators=[Optional()])
    submit = SubmitField('Submit Assessment')

# Helper functions
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You need to be an admin to access this page.', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        try:
            db.session.commit()
            flash('Your account has been created! You are now able to log in', 'success')
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            flash('That username or email is already taken. Please choose a different one.', 'danger')
    return render_template('register.html', title='Register', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    patients = Patient.query.all()
    assessments = Assessment.query.filter_by(date=datetime.date.today()).all()
    return render_template('dashboard.html', patients=patients, assessments=assessments)

@app.route('/search_patients')
@login_required
def search_patients():
    search_term = request.args.get('term', '')
    patients = Patient.query.filter(
        (Patient.first_name.ilike(f'%{search_term}%')) |
        (Patient.last_name.ilike(f'%{search_term}%')) |
        (Patient.email.ilike(f'%{search_term}%'))
    ).all()
    return jsonify([{'id': p.id, 'name': f"{p.first_name} {p.last_name}", 'email': p.email} for p in patients])

@app.route('/patients')
@login_required
def patient_list():
    patients = Patient.query.all()
    return render_template('patient_list.html', patients=patients)

@app.route('/add_patient', methods=['GET', 'POST'])
@login_required
def add_patient():
    form = PatientForm()
    if form.validate_on_submit():
        patient = Patient(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            date_of_birth=form.date_of_birth.data,
            email=form.email.data,
            phone=form.phone.data
        )
        db.session.add(patient)
        try:
            db.session.commit()
            flash('Patient added successfully!', 'success')
            return redirect(url_for('dashboard'))
        except IntegrityError:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'error')
    return render_template('add_patient.html', form=form)

@app.route('/assessment/<int:patient_id>', methods=['GET', 'POST'])
@login_required
def assessment(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    form = PatientAssessmentForm()
    
    if form.validate_on_submit():
        try:
            new_assessment = Assessment(
                patient_id=patient_id,
                facial_symmetry=form.facial_symmetry.data,
                profile_type=form.profile_type.data,
                lip_competence=form.lip_competence.data,
                profile_notes=form.profile_notes.data,
                breathing_pattern=form.breathing_pattern.data,
                swallowing_pattern=form.swallowing_pattern.data,
                speech_issues=form.speech_issues.data,
                functional_notes=form.functional_notes.data,
                pain=form.pain.data,
                clicking=form.clicking.data,
                range_of_motion=form.range_of_motion.data,
                tmj_notes=form.tmj_notes.data,
                teeth_condition=form.teeth_condition.data,
                gum_health=form.gum_health.data,
                occlusion=form.occlusion.data,
                intra_oral_notes=form.intra_oral_notes.data,
                diagnosis=form.diagnosis.data,
                treatment_objectives=form.treatment_objectives.data,
                proposed_treatment=form.proposed_treatment.data,
                estimated_duration=form.estimated_duration.data,
                treatment_notes=form.treatment_notes.data
            )
            db.session.add(new_assessment)
            db.session.commit()
            flash('Assessment submitted successfully!', 'success')
            return redirect(url_for('patient_details', patient_id=patient_id))
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error submitting assessment for patient {patient_id}: {str(e)}")
            flash('An error occurred while submitting the assessment. Please try again.', 'error')
    
    elif request.method == 'POST':
        logging.warning(f"Form validation failed for patient {patient_id}. Errors: {form.errors}")
        flash('There were errors in your submission. Please check the form and try again.', 'warning')
    
    return render_template('assessment.html', title='New Assessment', form=form, patient=patient)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/patient/<int:patient_id>')
@login_required
def patient_details(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    return render_template('patient_details.html', patient=patient)

# Admin routes
@app.route('/admin_panel')
@login_required
@admin_required
def admin_panel():
    return render_template('admin_panel.html')

@app.route('/get_users')
@login_required
@admin_required
def get_users():
    users = User.query.all()
    return jsonify([{"id": user.id, "username": user.username, "email": user.email, "is_admin": user.is_admin} for user in users])

@app.route('/add_user', methods=['POST'])
@login_required
@admin_required
def add_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    is_admin = data.get('is_admin', False)
    
    if not username or not email or not password:
        return jsonify({"success": False, "message": "Username, email, and password are required"}), 400
    
    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return jsonify({"success": False, "message": "Username or email already exists"}), 400
    
    new_user = User(username=username, email=email, is_admin=is_admin)
    new_user.set_password(password)
    db.session.add(new_user)
    
    try:
        db.session.commit()
        return jsonify({"success": True, "message": "User added successfully"})
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error adding user: {str(e)}")
        return jsonify({"success": False, "message": "An error occurred while adding the user"}), 500

@app.route('/update_user/<int:user_id>', methods=['PUT'])
@login_required
@admin_required
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    user.is_admin = data.get('is_admin', user.is_admin)
    
    if 'password' in data and data['password']:
        user.set_password(data['password'])
    
    try:
        db.session.commit()
        return jsonify({"success": True, "message": "User updated successfully"})
    except IntegrityError:
        db.session.rollback()
        return jsonify({"success": False, "message": "Username or email already exists"}), 400
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error updating user: {str(e)}")
        return jsonify({"success": False, "message": "An error occurred while updating the user"}), 500

@app.route('/delete_user/<int:user_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        return jsonify({"success": False, "message": "You cannot delete your own account"}), 400
    
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"success": True, "message": "User deleted successfully"})
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error deleting user: {str(e)}")
        return jsonify({"success": False, "message": "An error occurred while deleting the user"}), 500

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# Initialize Database
@app.cli.command('initdb')
def initdb_command():
    db.create_all()
    print('Initialized the database.')

if __name__ == '__main__':
    app.run(debug=True)