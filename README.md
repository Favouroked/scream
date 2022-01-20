# Scream Social Network

## Setup
### Prerequisites
* Python3

A virtualenv has to be setup to run this project. Follow the commands
below to set up the virtualenv and install the required libraries:
* Open the terminal in the project directory
* Run `python3 -m venv venv`
* Run `source venv/bin/activate`
* Finally, run `pip install -r requirement.txt` to install the required libraries.

### Environment Variable setup
The environment variables used in the project are specified in the `.env.sample` file. 
Create a `.env` in your root folder and add the environment variables as specified in the sample file.

### Migration
Before running the project for the first time, you have to apply migrations with the command below:
* `python manage.py migrate`

### Running the project
Run the command below to start the web server:
* `python manage.py runserver`

### Tests
Run the command below to run the tests in the project:
* `python manage.py test`

This will run all the tests in the django apps.

## Project Organisation
```
├── README.md
├── config
│   ├── __init__.py
│   ├── request.py
│   └── secrets.py
├── db.sqlite3
├── manage.py
├── posts
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_rename_likes_like.py
│   │   └── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── requirements.txt
├── scream
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── users
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── auth.py
    ├── migrations
    │   ├── 0001_initial.py
    │   ├── 0002_user_signup_holiday.py
    │   └── __init__.py
    ├── models.py
    ├── serializers.py
    ├── tests.py
    ├── urls.py
    ├── utils.py
    └── views.py
```