# CampusBridge Quick Start and Developer Guide

**CS 530 Spring 2026, Team Robotastic**

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

4. Open `http://127.0.0.1:8000` and you should see a Django success screen

5. To stop the Django server, input Ctrl+C
6. To deactivate venv, run `deactivate`

*Once project is setup, you can run the project by sourcing the venv and using* `python manage.py runserver`.


## Updating Database Models
If you are doing database work and change any models, you MUST run:
```
python manage.py makemigrations
python manage.py migrate
```

Any migration files that are created MUST be committed to GitHub so all team members can recreate the same database on their local machine. Do not commit db.sqlite3.


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