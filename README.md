# MY_Sight

A Django-based application for managing patient-companion relationships and medical reminders.

## Project Structure

```
MY_Sight/
├── MY_Sight/                 # Project configuration directory
│   ├── __init__.py
│   ├── settings.py          # Project settings
│   ├── urls.py             # Main URL configuration
│   ├── asgi.py             # ASGI configuration
│   └── wsgi.py             # WSGI configuration
│
├── Users/                   # Users app directory
│   ├── __init__.py
│   ├── admin.py            # Admin configuration
│   ├── apps.py             # App configuration
│   ├── models.py           # Database models
│   ├── serializers.py      # API serializers
│   ├── tasks.py            # Celery tasks
│   ├── urls.py             # App URL configuration
│   └── views.py            # API views
│
├── static/                  # Static files directory
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/              # HTML templates
│   └── password_reset_confirm.html
│
├── manage.py              # Django management script
├── requirements.txt       # Project dependencies
└── README.md             # Project documentation
```

## Key Files Description

### Project Configuration
- `MY_Sight/settings.py`: Contains all project settings including:
  - Database configuration
  - Installed apps
  - Middleware settings
  - Static files configuration
  - Email settings
  - JWT settings
  - CORS settings

### Users App
- `Users/models.py`: Contains database models:
  - User (Custom user model)
  - Patient
  - Companion
  - Task
  - Reminder
  - Location
  - Notification

- `Users/serializers.py`: API serializers for:
  - User registration and profile
  - Patient profile
  - Companion profile
  - Task management
  - Location tracking
  - Notifications

- `Users/views.py`: API endpoints for:
  - User authentication
  - Profile management
  - Task management
  - Location tracking
  - Notifications

- `Users/tasks.py`: Celery tasks for:
  - Task reminders
  - Email notifications

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/password-reset/` - Password reset request
- `POST /api/auth/password-reset-confirm/` - Password reset confirmation

### Profile Management
- `GET/PATCH /api/profile/` - Get/Update user profile
- `GET/PATCH /api/companion-profile/` - Get/Update companion profile
- `GET/PATCH /api/patient-profile/` - Get/Update patient profile

### Tasks and Reminders
- `GET/POST /api/tasks/` - List/Create tasks
- `GET/PUT/DELETE /api/tasks/<id>/` - Get/Update/Delete specific task
- `GET/POST /api/reminders/` - List/Create reminders

### Location Tracking
- `GET/POST /api/locations/` - List/Create location records
- `GET/PUT/DELETE /api/locations/<id>/` - Get/Update/Delete specific location

### Notifications
- `GET /api/notifications/` - List notifications
- `GET/PUT /api/notifications/<id>/` - Get/Update specific notification

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/Usef3/MY_Sight.git
cd MY_Sight
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Run the development server:
```bash
python manage.py runserver
```

## Technologies Used

- **Backend Framework**: Django
- **API Framework**: Django REST Framework
- **Authentication**: JWT (JSON Web Tokens)
- **Task Queue**: Celery with Redis
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **Email**: SMTP (Gmail)
- **API Documentation**: Swagger/OpenAPI

## Features

- User authentication (Patients and Companions)
- Profile management
- Patient-Companion relationship management
- Medical reminders and tasks
- Location tracking
- Notifications system
- Email notifications
- Real-time task reminders


