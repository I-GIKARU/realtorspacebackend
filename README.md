# RealtorSpace - Property Management System

## Project Overview
RealtorSpace is a comprehensive property management system built with Django that enables real estate agencies and property managers to efficiently manage their property listings, track amenities, and organize property information. This platform provides a robust RESTful API for accessing property data and supports secure user authentication for property management.

## Features
- **Property Listings**: Create, read, update, and delete property listings with detailed information
- **Property Images**: Upload and manage multiple images for each property using Cloudinary storage
- **Amenities Management**: Track and filter properties by available amenities
- **User Authentication**: Secure JWT authentication system for users and property managers
- **RESTful API**: Comprehensive API for integrating with mobile apps or other services
- **Admin Dashboard**: User-friendly admin interface using Django Jazzmin for property management
- **Responsive Design**: Mobile-friendly interface for accessing properties on any device
- **Search & Filtering**: Advanced search and filtering options for property listings

## Technologies Used
- **Backend**: Django 4.2, Django REST Framework
- **Database**: PostgreSQL (Neon DB for production)
- **Authentication**: JWT (JSON Web Tokens)
- **File Storage**: Cloudinary for media files, WhiteNoise for static files
- **Deployment**: Render.com
- **API Documentation**: Swagger/OpenAPI using drf-yasg
- **Styling**: Django Jazzmin for admin interface
- **Development Tools**: Django Debug Toolbar

## Local Development Setup

### Prerequisites
- Python 3.12+
- PostgreSQL (optional for local development, SQLite can be used instead)
- Git

### Installation Steps
1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/realtorspace.git
   cd realtorspace
   ```

2. Create and activate a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root directory with the necessary environment variables (see Environment Variables section)

5. Run migrations
   ```bash
   python manage.py migrate
   ```

6. Create a superuser
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server
   ```bash
   python manage.py runserver
   ```

8. Access the application at http://127.0.0.1:8000/

## Environment Variables
Create a `.env` file in the project root directory with the following variables:

```
# Django Settings
DJANGO_SECRET_KEY=your_secret_key
DEBUG=True  # Set to False in production
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
# For SQLite (local development): DATABASE_URL=sqlite:///db.sqlite3

# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# For Production
CSRF_TRUSTED_ORIGINS=https://*.yourdomain.com,https://*.onrender.com
```

## Deployment on Render.com

### Prerequisites
- A Render.com account
- A GitHub/GitLab repository with your project

### Deployment Steps
1. Push your code to a Git repository (GitHub/GitLab)

2. Login to your Render.com account and create a new Web Service

3. Connect to your Git repository

4. Configure the service:
   - **Environment**: Python
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn core.wsgi:application`

5. Add the following environment variables in the Render dashboard:
   - `DJANGO_SECRET_KEY`: A strong random key
   - `DEBUG`: False
   - `ALLOWED_HOSTS`: yourdomain.com,*.onrender.com
   - `CSRF_TRUSTED_ORIGINS`: https://*.yourdomain.com,https://*.onrender.com
   - `DATABASE_URL`: Your Neon PostgreSQL connection URL
   - `CLOUDINARY_CLOUD_NAME`: Your Cloudinary cloud name
   - `CLOUDINARY_API_KEY`: Your Cloudinary API key
   - `CLOUDINARY_API_SECRET`: Your Cloudinary API secret

6. Click "Create Web Service" and wait for the deployment to complete

7. Your application will be available at the provided Render URL

## Database Setup

### Local Development
By default, the application uses SQLite for local development. To use PostgreSQL locally:

1. Install PostgreSQL on your system
2. Create a new database and user
3. Update the `DATABASE_URL` in your `.env` file

### Production (Neon PostgreSQL)
The application is configured to use Neon PostgreSQL in production:

1. Create a Neon PostgreSQL database
2. Get the connection URL from Neon dashboard
3. Add it as the `DATABASE_URL` environment variable in Render

## Static Files and Media Storage

### Static Files
Static files are managed using WhiteNoise in production:

- During deployment, `python manage.py collectstatic` collects all static files to the `staticfiles` directory
- WhiteNoise serves these files efficiently in production

### Media Files
Media files (like property images) are stored in Cloudinary:

1. Create a Cloudinary account
2. Configure your Cloudinary credentials in the environment variables
3. The Django Cloudinary Storage package handles uploads and serving of media files

## Project Structure
```
realtorspace/
├── core/                  # Project settings and main configuration
│   ├── settings.py        # Project settings
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py            # WSGI configuration for deployment
├── properties/            # Property management app
│   ├── models.py          # Property and related models
│   ├── views.py           # API views for property management
│   ├── serializers.py     # DRF serializers
│   └── urls.py            # Property app URL patterns
├── static/                # Static files (CSS, JS, images)
├── templates/             # HTML templates
├── property_images/       # Directory for uploaded property images (local dev)
├── manage.py              # Django management script
├── requirements.txt       # Project dependencies
├── build.sh               # Build script for Render deployment
├── Procfile               # Process file for Render deployment
└── .env                   # Environment variables (not in version control)
```

## Contributing
Contributions to RealtorSpace are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests to ensure everything works
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

---

© 2025 RealtorSpace. All rights reserved.

