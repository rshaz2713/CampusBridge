# CampusBridge Quick Start and Developer Guide

**Team Robotastic — CS 530 Spring 2026**

**FOR** institutions of higher education<br>
**WHERE** professors and students need a centralized gateway for campus essentials,<br>
**THE** CampusBridge<br>
**IS** a responsive web-based university pipeline<br>
**THAT** incorporates an intuitive UI, allowing users to focus on learning, teaching, and research rather than navigating fragmented systems.<br>
**UNLIKE** the Ellucian CentralPipeline,<br>
**OUR PRODUCT** prioritizes usability, minimal navigation friction, and system reliability.<br>

## Project Setup

**Note that Python 3.13.5 was used to create the Django project. Please install it or any similar version.**

To setup the project:
1. Clone repository to your local machine
2. Verify Python is installed
3. Run the following:
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
*NOTE: If you are using Windows Terminal, to source the venv run* `.\venv\Scripts\Activate.ps1`.

4. Open `http://127.0.0.1:8000` and you should see the landing page for CampusBridge
5. To stop the Django server, input Ctrl+C
6. To deactivate venv, run `deactivate`

*Note that once you have completed project setup, you can run the project anytime by sourcing the venv and using* `python manage.py runserver`.

## Project Structure

Directory Overview:
* `config/` - Global Django configuration
* `core/` - Django app for landing page and general site pages that are shared
* `dashboard/` - Django app for authenticated dashboard views
* `templates/` - HTML templates rendered by views

Authentication:
* CampusBridge uses Django's built-in authentication framework (django.contrib.auth). This proivdes login, logout, session management, and password validation for us.
* Django provides URL routes `/accounts/login/` and `/accounts/logout/` for login and logout.
* Views requiring login are protected by Django's `@login_required` decorator, automatically redirecting the user to login.

## Adding a Page

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

## Superusers

For development purposes, you should create a superuser to access Django admin via `http://127.0.0.1:8000/admin` and to test login/logout features.

In your venv, run `python manage.py createsuperuser` and set a dummy name, email, and password. This will be stored in your local database and will not be committed to GitHub.

## Updating Database Models

If you are doing database work and change any models, you MUST run:
```
python manage.py makemigrations
python manage.py migrate
```

Any migration files that are created MUST be committed to GitHub so all team members can recreate the same database on their local machine.

**Do not commit db.sqlite3 to GitHub.**

## Git Practices

* No direct commits to `main`
* Verify you have access to `.gitignore`
* Create branches as `type/short-description`. Types:
    * `feat/` - New user-facing capability
    * `fix/` - Bug fix
    * `chore/` - Setup, tooling, dependencies, refactors, formatting
    * `docs/` - Documentation only
* Open pull requests when completed with branch work
* We will mostly use squash and merge
* Verify main still works
* Never commit `venv/`, `.env`, or `db.sqlite3`