# CampusBridge Quick Start and Developer Guide

**Team Robotastic — CS 530 Spring 2026**

**FOR** institutions of higher education<br>
**WHERE** professors and students need a centralized gateway for campus essentials,<br>
**THE** CampusBridge<br>
**IS** a responsive web-based university pipeline<br>
**THAT** incorporates an intuitive UI, allowing users to focus on learning, teaching, and research rather than navigating fragmented systems.<br>
**UNLIKE** the Ellucian CentralPipeline,<br>
**OUR PRODUCT** prioritizes usability, minimal navigation friction, and system reliability.<br>

## 1. Project Structure

Directory Overview:
* `config/` - Global Django configuration
* `core/` - Django app for landing page and general site pages that are shared
* `dashboard/` - Django app for authenticated dashboard views
* `templates/` - HTML templates rendered by views
* `static/` - Static CSS and JS files

Authentication:
* CampusBridge uses Django's built-in authentication framework (django.contrib.auth). This proivdes login, logout, session management, and password validation for us.
* Django provides URL routes `/accounts/login/` and `/accounts/logout/` for login and logout.
* Views requiring login are protected by Django's `@login_required` decorator, automatically redirecting the user to login.
* Each login session lasts 60 seconds, extendable by clicking the pop up button at the bottom, refreshing the page, or clicking a link. Upon expiry, you will have to login again.

## 2. Project Setup

### 2a. Setting up the System

**Note that Python 3.13.5 was used to create the Django project. Please install it or any similar version.**

1. Clone repository to your local machine
2. Verify Python is installed
3. Run the following:
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
*NOTE: If you are using Windows Terminal, to source the venv run* `.\venv\Scripts\Activate.ps1`.

4. Open `http://127.0.0.1:8000` and you should see the landing page for CampusBridge
5. To stop the Django server, input Ctrl+C
6. To deactivate venv, run `deactivate`

*Note that once you have completed project setup, you can run the project anytime by sourcing the venv and using* `python manage.py runserver`.

### 2b. Setting up Basic CampusBridge Features

CampusBridge as a prototype supports basic registration, grade input, and degree audits for courses. In this prototype, a professor who is a department chair will have to be assigned as a superuser, and any preliminary course info will be configured in the Django admin. In a future iteration, a university admin/registrar role can be added in CampusBridge to handle this. For now, follow these steps:

1. Start the Django server. Go to CampusBridge and make a professor account
3. Stop the Django server, and run `python manage.py shell`. You will now make this professor a superuser via the Python command line
4. Run the following:

```
from django.contrib.auth.models import User
User.objects.all()
user = User.objects.get(username = "user Name of the Depart Chair")
user.is_staff = True
user.is_superuser = True
user.save()
exit()
```

5. Start the Django server and login to the admin portal at `http://127.0.0.1:8000/admin` with this professor's credentials.
6. In the list of tables for the Dashboard app, find the courses table and click "Add". Fill out the info and assign a professor(s) to it (this can be any professor account that is registered in CampusBridge). If you want to create multiple sections, repeat this process and assign a different number. This is an example Course input:
```
Course code: "CS 530"
Course name: "Advanced Software Engineering"
Semester: "Spring 2026"
Section: "01"
```

7. Now when you log into CampusBridge as a professor, you can see your courses and the roster of students. If you login as a student, you can see available courses and enroll/withdraw.

## 3. Adding a Page

**FYI, you should not have to edit config files or settings. These steps should be sufficient.**

1. Create an HTML template inside `templates`; make sure to put in appropriate subdirectory. Use Django syntax to construct your HTML template. Example:
```
{% extends "base.html" %}
{% block title %}Title{% endblock %}
{% block content %}
<h1>Heading</h1>
<p>Paragraph</p>
{% endblock %}
```

2. Add the view in a `views.py` file. If it's a general app view, add in `core/views.py`; if it's a dashboard view, add in `dashboard/views.py`. This view function is what will render the template. If it's authentication-protected, add decorator `@login_required`.

3. Add the route in `urls.py` for the corresponding application. (You should not have to touch `config/urls.py`; that is for global routing.)

4. Test by running the project as mentioned above.

## 4. Updating Database Models

If you are doing database work and change any models, you MUST run:
```
python manage.py makemigrations
python manage.py migrate
```

Any migration files that are created MUST be committed to GitHub so all team members can recreate the same database on their local machine.

**Do not commit db.sqlite3 to GitHub.**

## 5. Git Practices

* No direct commits to `main`
* Verify you have access to `.gitignore`
* Create branches with the format `type/short-description`. Types of branches include:
    * `feat/` - New user-facing capability
    * `fix/` - Bug fix
    * `chore/` - Setup, tooling, dependencies, refactors, formatting
    * `docs/` - Documentation only
    * Example branch names: `feat/grades-view`, `chore/django-setup`, `docs/auth-info`
* Open pull requests when completed with branch work
* We will mostly use squash and merge
* Verify main still works
* Never commit `venv/`, `.env`, or `db.sqlite3`