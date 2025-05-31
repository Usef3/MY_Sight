# MY_Sight

A Django-based application for managing patient-companion relationships and medical reminders.

## Features

- User authentication (Patients and Companions)
- Profile management
- Patient-Companion relationship management
- Medical reminders and tasks
- Location tracking
- Notifications system

## Setup

1. Clone the repository:
```bash
git clone https://github.com/your-username/MY_Sight.git
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

## API Endpoints

- `/api/profile/` - Profile management
- `/api/auth/` - Authentication endpoints
- `/api/tasks/` - Task management
- `/api/notifications/` - Notification system

## Technologies Used

- Django
- Django REST Framework
- Celery
- Redis
- JWT Authentication 