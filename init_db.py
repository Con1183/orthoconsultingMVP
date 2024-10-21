from app import app, db, User, Patient, Assessment
from werkzeug.security import generate_password_hash
from datetime import datetime
import os
import logging
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_admin_user():
    admin_username = os.getenv('ADMIN_USERNAME', 'admin')
    admin_email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
    admin_password = os.getenv('ADMIN_PASSWORD', 'password123')  # Use a secure password in production

    try:
        admin_user = User.query.filter_by(username=admin_username).first()
        if admin_user is None:
            admin_user = User(username=admin_username, email=admin_email, is_admin=True)
            admin_user.set_password(admin_password)
            db.session.add(admin_user)
            db.session.commit()
            logging.info(f"Admin user created. Username: {admin_username}, Email: {admin_email}")
        else:
            logging.info("Admin user already exists.")
    except Exception as e:
        logging.error(f"Error creating admin user: {str(e)}")
        db.session.rollback()

def create_sample_patient():
    try:
        sample_patient = Patient(
            first_name="John",
            last_name="Doe",
            date_of_birth=datetime(1990, 1, 1).date(),
            email="john.doe@example.com",
            phone="123-456-7890"
        )
        db.session.add(sample_patient)
        db.session.commit()

        sample_assessment = Assessment(
            patient_id=sample_patient.id,
            date=datetime.now().date(),
            facial_symmetry="Symmetrical",
            profile_type="Straight",
            lip_competence="Competent",
            profile_notes="No significant asymmetry noted",
            breathing_pattern="Nasal",
            swallowing_pattern="Normal",
            speech_issues="None",
            functional_notes="Normal function observed",
            pain="None",
            clicking="Absent",
            range_of_motion="Normal",
            tmj_notes="No TMJ issues detected",
            teeth_condition="Healthy",
            gum_health="Healthy",
            occlusion="Class I",
            intra_oral_notes="No significant issues noted",
            diagnosis="Healthy patient with no significant orthodontic issues",
            treatment_objectives="Maintain current oral health",
            proposed_treatment="Regular check-ups recommended",
            estimated_duration="N/A",
            treatment_notes="Patient advised on proper oral hygiene techniques"
        )
        db.session.add(sample_assessment)
        db.session.commit()

        logging.info("Sample patient and assessment added successfully.")
    except Exception as e:
        logging.error(f"Error creating sample patient and assessment: {str(e)}")
        db.session.rollback()

def create_test_patient():
    try:
        test_patient = Patient(
            first_name="Jane",
            last_name="Smith",
            date_of_birth=datetime(1985, 5, 15).date(),
            email="jane.smith@example.com",
            phone="987-654-3210"
        )
        db.session.add(test_patient)
        db.session.commit()
        logging.info("Test patient added successfully.")
    except Exception as e:
        logging.error(f"Error creating test patient: {str(e)}")
        db.session.rollback()

def init_database():
    db_file = 'orthodontic.db'
    if os.path.exists(db_file):
        response = input(f"The database file '{db_file}' already exists. Do you want to reset it? (y/n): ")
        if response.lower() == 'y':
            os.remove(db_file)
            logging.info(f"Existing database '{db_file}' has been deleted.")
        else:
            logging.info("Database reset cancelled. Exiting.")
            return

    with app.app_context():
        try:
            db.create_all()
            logging.info("Database tables created.")

            create_admin_user()

            if Patient.query.first() is None:
                create_sample_patient()

            if not Patient.query.filter_by(email="jane.smith@example.com").first():
                create_test_patient()
            else:
                logging.info("Test patient already exists.")

            logging.info("Database initialization completed.")
        except Exception as e:
            logging.error(f"Error during database initialization: {str(e)}")
            sys.exit(1)

if __name__ == "__main__":
    init_database()