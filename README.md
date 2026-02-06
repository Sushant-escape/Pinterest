# Pinterest Clone

A Django-based Pinterest clone application with features for user authentication, pin management, and boards.

## Features

- User Registration & Authentication
- User Profiles
- Create, Read, Update, Delete Pins
- Boards Management
- User Follow/Unfollow
- Pin Likes
- Search Functionality

## Project Structure

```
Pinterest/
├── manage.py
├── requirements.txt
├── .env
├── MyProject/              # Main configuration
├── apps/
│   ├── accounts/           # User authentication & profiles
│   ├── pins/               # Pin management
│   ├── boards/             # Board management
│   └── core/               # Core functionality (home, explore)
├── templates/              # HTML templates
├── static/                 # CSS, JS, Images
├── media/                  # User uploads
└── README.md
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Pinterest
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   - Copy `.env.example` to `.env`
   - Update settings as needed

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## Usage

- Access the application at `http://127.0.0.1:8000/`
- Admin panel: `http://127.0.0.1:8000/admin/`

## Technologies

- Django 6.0.2
- Python 3.x
- SQLite (default)
- Pillow (Image handling)

## License

MIT License
