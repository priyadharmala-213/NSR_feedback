# NSRIT College Feedback System

A comprehensive web-based feedback and complaint management system for NSRIT College, supporting multiple branches, semesters, and different types of academic feedback.

## Features

### Student Module
- **User Registration & Authentication**: Secure registration with email verification
- **Branch & Semester Selection**: Dynamic selection of academic structure
- **Subject-wise Feedback**: Rate and provide feedback on:
  - Subject Quality
  - Faculty Performance
  - Lab/Practical Work
  - Project Guidance
  - Internship Experience
- **Complaint Management**: Submit and track complaints
- **5-Star Rating System**: Comprehensive feedback collection

### Admin Module
- **Dashboard Analytics**: Real-time statistics on feedbacks and complaints
- **Advanced Filtering**: Filter by:
  - Branch
  - Semester
  - Subject
- **Complaint Management**: Review, track, and resolve student complaints
- **Export Ready**: Data structured for analytics and reporting

## Supported Branches
- CSE (Computer Science)
- CSE-AI&ML (AI & Machine Learning)
- CSE-DS (Data Science)
- ECE (Electronics & Communication)
- EEE (Electrical & Electronics)
- Mechanical Engineering
- Civil Engineering

## Supported Semesters
Semesters 1-8 with complete subject mapping for each branch

## Technology Stack
- **Backend**: Python Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3
- **Authentication**: Werkzeug security (password hashing)

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone/Download the Project
```bash
cd NSR_feedback
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

## Default Admin Credentials
- **Email**: admin@nsrit.edu
- **Password**: admin123

**Note**: Change these credentials immediately after first login!

## Project Structure
```
NSR_feedback/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── feedback_system.db              # SQLite database (auto-created)
├── templates/
│   ├── index.html                  # Homepage with login portals
│   ├── student_login.html          # Student login page
│   ├── student_register.html       # Student registration
│   ├── student_dashboard.html      # Student main dashboard
│   ├── feedback_form.html          # Feedback submission form
│   ├── complaint_form.html         # Complaint submission form
│   ├── admin_login.html            # Admin login page
│   ├── admin_dashboard.html        # Admin dashboard with analytics
│   ├── admin_feedbacks.html        # View feedbacks with filters
│   ├── admin_complaints.html       # Manage complaints
│   └── static/
│       └── style.css               # Global styles
└── README.md                       # This file
```

## Database Models

### User
- Email (unique)
- Password (hashed)
- User Type (student/admin)
- Name
- Roll Number (students only)
- Branch (students)
- Semester (students)

### Branch
- Name (CSE, ECE, etc.)
- Code (unique identifier)

### Semester
- Number (1-8)

### Subject
- Name
- Code
- Branch ID
- Semester ID
- Subject Type (theory, lab, elective, project, internship, mandatory)
- Elective Group (for dynamic electives)
- Faculty ID
- Credits

### Feedback
- Student ID
- Subject ID
- Feedback Type (subject, faculty, lab, project, internship)
- Rating (1-5)
- Comments
- Created At (timestamp)

### Complaint
- Student ID
- Subject
- Description
- Status (open, in_progress, resolved)
- Created At
- Resolved At

## User Workflows

### Student Workflow
1. Register with email and password
2. Login to dashboard
3. Select branch and semester
4. Choose subjects for feedback
5. Submit feedback with rating and comments
6. (Optional) Submit complaints if issues arise

### Admin Workflow
1. Login with admin credentials
2. View dashboard statistics
3. View all feedbacks with advanced filtering
4. Review student complaints
5. Track complaint resolution status

## API Endpoints

### Public Routes
- `GET /` - Homepage
- `GET/POST /student-login` - Student login
- `GET/POST /student-register` - Student registration
- `GET/POST /admin-login` - Admin login

### Student Routes (Protected)
- `GET /student/dashboard` - Student dashboard
- `POST /student/select-branch` - Update branch/semester
- `GET /student/feedback` - View feedback form
- `POST /student/submit-feedback` - Submit feedback
- `GET/POST /student/complaint` - Submit complaint

### Admin Routes (Protected)
- `GET /admin/dashboard` - Admin dashboard with stats
- `GET /admin/feedbacks` - View all feedbacks with filters
- `GET /admin/complaints` - View all complaints

### Common Routes
- `GET /logout` - Logout user

## Features Implementation

### Authentication
- Password hashing using Werkzeug
- Session management with Flask sessions
- Role-based access control (student/admin)

### Subject Mapping
- Dynamic subject loading based on branch and semester
- Support for 7 branches and 8 semesters
- Flexible elective group support

### Feedback System
- Multiple feedback types (subject, faculty, lab, project, internship)
- 5-star rating system
- Optional detailed comments
- Timestamp tracking

### Analytics & Filtering
- Filter feedbacks by branch, semester, subject
- View complaint status and timestamps
- Real-time statistics dashboard

## Future Enhancements

1. **Advanced Analytics**
   - Charts and graphs for feedback trends
   - Department-wise performance comparison

2. **Email Notifications**
   - Complaint status updates
   - Feedback submission confirmations

3. **Faculty Portal**
   - View feedback specific to their subjects
   - Performance metrics

4. **Export Features**
   - Export feedbacks to CSV/PDF
   - Generate reports

5. **Improved Complaint Management**
   - Status update notifications
   - Resolution time tracking

6. **Multi-language Support**
   - Telugu and Hindi interfaces

## Security Notes

1. **Always change default admin credentials** after first login
2. Database file (`feedback_system.db`) should be backed up regularly
3. Use HTTPS in production environments
4. Consider implementing CSRF protection for production

## Troubleshooting

### Database Issues
If you encounter database errors, delete `feedback_system.db` and restart the application. It will recreate the database with initial data.

### Import Errors
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Port Already in Use
If port 5000 is already in use, modify the last line in `app.py`:
```python
app.run(debug=True, port=5001)  # Use different port
```

## Support & Contact
For issues and feature requests, please contact the development team.

## License
This project is proprietary to NSRIT College. All rights reserved.

## Version
1.0.0 - Initial Release

---
**Created**: 2024
**Last Updated**: April 2026
