# 🦷 Orthodontic Consulting MVP 🦷

Welcome to the Orthodontic Consulting MVP — a comprehensive web application designed for managing patients, their orthodontic assessments, and administrative tasks with ease!

This application provides user authentication, patient record management, orthodontic assessments, and an admin panel for user management.

## ✨ Features

- 👤 User Authentication: Register, log in, and manage users securely.
- 📝 Patient Management: Add, view, and edit patient information easily.
- 📊 Assessment Management: Record, update, and view detailed orthodontic assessments for each patient.
- 🖥 Dashboard: See an overview of today's assessments and patient data at a glance.
- 🔐 Admin Panel: Manage user accounts, including adding/removing admin privileges.

## 🛠 Technologies

- Python 3.9+
- Flask (Web Framework)
- Flask-SQLAlchemy (ORM)
- Flask-Login (User Authentication)
- SQLite (Database)
- Flask-WTF (Form Handling)
- Tailwind CSS (Styling)
- HTML for front-end templates
- JavaScript for dynamic interactions

## 🚀 Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/orthodontic-consulting-mvp.git
cd orthodontic-consulting-mvp
```

### 2️⃣ Create a Virtual Environment and Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

### 3️⃣ Configure the Application

Create a `.env` file in the root directory and add:

```
SECRET_KEY=your_secret_key_here
DATABASE_URI=sqlite:///orthodontic.db
```

Replace `your_secret_key_here` with a secure random string.

### 4️⃣ Initialize the Database

```bash
flask initdb
```

This will create all necessary tables (User, Patient, Assessment).

### 5️⃣ Run the Application

```bash
flask run
```

By default, the app will run on http://127.0.0.1:5000/.

## 🌐 Available Routes

- `/`: Dashboard showing today's assessments.
- `/login`: Login page.
- `/logout`: Log out of the app.
- `/add_patient`: Add a new patient.
- `/patient/<int:patient_id>`: View patient details.
- `/assessment/<int:patient_id>`: Record or view patient assessments.
- `/admin_panel`: Admin panel for user management (admin access required).

## 📦 Database Models

### User
- id: Integer, Primary Key
- username: String, unique, required
- email: String, unique, required
- password: String, hashed
- is_admin: Boolean, default False

### Patient
- id: Integer, Primary Key
- first_name: String, required
- last_name: String, required
- date_of_birth: Date, required
- email: String, unique, required
- phone: String

### Assessment
- id: Integer, Primary Key
- patient_id: Foreign Key linked to Patient
- date: Date of assessment (default is today)
- facial_symmetry: String
- profile_type: String
- lip_competence: String
- breathing_pattern: String
- swallowing_pattern: String
- speech_issues: String
- pain: String
- clicking: String
- range_of_motion: String
- teeth_condition: String
- gum_health: String
- occlusion: String
- diagnosis: Text
- treatment_objectives: Text
- proposed_treatment: Text
- estimated_duration: String

## 📝 Usage Guide

### Logging In
1. Navigate to the login page.
2. Enter your username and password.
3. Click "Login" to access the dashboard.

### Adding a New Patient
1. From the dashboard, click "Add New Patient".
2. Fill in the patient's details (name, date of birth, contact information).
3. Click "Add Patient" to save the record.

### Conducting an Assessment
1. Search for a patient or select from the patient list.
2. Click on the patient's name to view their profile.
3. Select "New Assessment" from the patient's profile.
4. Fill in the comprehensive assessment form.
5. Click "Submit Assessment" to save the record.

### Using the Admin Panel
1. Log in with an admin account.
2. Navigate to the Admin Panel from the dashboard.
3. Here you can view all user accounts, add new users, delete existing users, and modify user roles.

## 🔒 Security Considerations

- Always use HTTPS in production environments.
- Regularly update the application and its dependencies.
- Use strong, unique passwords for all accounts, especially admin accounts.
- Implement proper input validation and sanitization to prevent XSS and SQL injection attacks.
- Regularly backup the database.

## 🐛 Troubleshooting

- If you encounter a "csrf_token is undefined" error, ensure that Flask-WTF is properly installed and configured in your application.
- For database-related issues, check the database connection string in your configuration.
- If you're having trouble with user authentication, verify that the user's credentials are correct and that their account hasn't been deactivated.

## 🤝 Contributing

We welcome contributions to improve the Orthodontic Consulting MVP. Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with clear, descriptive messages.
4. Push your changes to your fork.
5. Submit a pull request with a detailed description of your changes.

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

## 🌟 Future Enhancements

- 📊 Add data visualization for patient progress.
- 📱 Develop a mobile app version for on-the-go access.
- 🔗 Integrate with popular practice management software.
- 🤖 Implement AI-assisted treatment planning suggestions.

Now you're ready to efficiently manage patients, conduct detailed orthodontic assessments, and streamline your orthodontic consulting practice! 🦷✨