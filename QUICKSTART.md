# NSRIT Feedback System - Quick Start Guide

## ⚡ Getting Started in 5 Minutes

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python app.py
```

### 3. Open in Browser
Navigate to: **http://localhost:5000**

---

## 🎓 For Students

### First Time Setup
1. Click **"Register"** on the Student Portal
2. Fill in your details:
   - Full Name
   - College Email
   - Roll Number
   - Password (minimum 8 characters recommended)
3. Click **"Register"**
4. Return to login and enter credentials

### Submitting Feedback
1. Click **"Student Login"**
2. Select your **Branch** and **Semester**
3. Click **"Go to Feedback Form"**
4. Select a subject and feedback type
5. Rate (1-5 stars) and add comments if desired
6. Click **"Submit Feedback"**

### Submitting Complaints
1. From Student Dashboard, click **"Submit Complaint"**
2. Enter complaint subject and detailed description
3. Click **"Submit Complaint"**
4. Your complaint will be tracked by admin

---

## 👨‍💼 For Administrators

### Login Credentials
- **Email**: admin@nsrit.edu
- **Password**: admin123

### Accessing the Dashboard
1. Click **"Admin Login"** on homepage
2. Enter credentials
3. View real-time statistics:
   - Total Feedbacks
   - Total Complaints
   - Active Students
   - Number of Branches

### Viewing Feedbacks
1. From dashboard, click **"View All Feedbacks"**
2. Use filters:
   - Branch
   - Semester
   - Subject
3. View detailed feedback with ratings and comments

### Managing Complaints
1. From dashboard, click **"View Complaints"**
2. Filter by status: Open, In Progress, Resolved
3. Review complaint details
4. Update status as needed

---

## 📊 Key Features

### Student Features
✅ Secure registration with email  
✅ Dynamic branch and semester selection  
✅ Multiple feedback types (subject, faculty, lab, project, internship)  
✅ 5-star rating system  
✅ Optional detailed comments  
✅ Complaint submission and tracking  

### Admin Features
✅ Real-time dashboard analytics  
✅ Advanced filtering capabilities  
✅ Complaint management system  
✅ View all feedbacks with details  
✅ Status tracking for complaints  
✅ Export-ready data structure  

---

## 🗂️ Project Structure

```
NSR_feedback/
├── app.py                    ← Main application (RUN THIS)
├── requirements.txt          ← Dependencies
├── feedback_system.db        ← Database (auto-created)
├── README.md                 ← Full documentation
├── QUICKSTART.md            ← This file
├── .gitignore               ← Git configuration
└── templates/
    ├── index.html                    (Homepage)
    ├── student_login.html            (Student login)
    ├── student_register.html         (Student registration)
    ├── student_dashboard.html        (Student dashboard)
    ├── feedback_form.html            (Feedback submission)
    ├── complaint_form.html           (Complaint submission)
    ├── admin_login.html              (Admin login)
    ├── admin_dashboard.html          (Admin dashboard)
    ├── admin_feedbacks.html          (View feedbacks)
    ├── admin_complaints.html         (Manage complaints)
    └── static/
        └── style.css                 (Styling)
```

---

## 🔐 Security Tips

⚠️ **IMPORTANT**: Change the default admin password immediately!

1. Login with default credentials (admin@nsrit.edu / admin123)
2. Modify the password in the User table (or re-register with new email)
3. Update the admin credentials

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Database errors | Delete `feedback_system.db` and restart app |
| Port 5000 in use | Change port in `app.py`: `app.run(port=5001)` |
| Import errors | Run: `pip install -r requirements.txt` |
| Cannot access pages | Ensure you're logged in with correct role |

---

## 📝 Sample Data

### Pre-loaded Branches
- CSE (Computer Science)
- CSE-AI&ML (AI & Machine Learning)
- CSE-DS (Data Science)
- ECE (Electronics & Communication)
- EEE (Electrical & Electronics)
- Mechanical
- Civil

### Pre-loaded Semester 1 Subjects (All Branches)
- Linear Algebra and Calculus
- Engineering Physics/Chemistry
- Basics of Civil and Mechanical Engineering
- Engineering Graphics
- Problem Solving Using C
- Physics/Chemistry Lab
- C Programming Lab
- Engineering Workshop Practice

---

## 🚀 Next Steps

1. **Customize**: Update college logo, colors, and branding
2. **Populate**: Add more subjects for other semesters
3. **Deploy**: Use gunicorn or uWSGI for production
4. **Backup**: Regularly backup the database
5. **Extend**: Add faculty portal, email notifications, analytics

---

## 📞 Support

For technical issues or feature requests, contact the development team.

**Version**: 1.0.0  
**Last Updated**: April 2026
