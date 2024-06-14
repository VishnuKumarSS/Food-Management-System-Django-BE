# Food Management System

## Tech Stack
<code>Python</code>
<code>Django</code>
<code>Javascript</code>
<code>React</code>
<code>Tailwind</code>

## Server side configurations

#### 1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

#### 2. Install dependencies:
```bash
pip install -r requirements.txt
```

#### 3. Run and Load migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 4. Start the development server:

```bash
python manage.py runserver
```

## Server side utilities

#### 1. Create normaluser and superuser:
```bash
python manage.py createsuperuser

# Or we can create users programatically by opening interactive shell
python manage.py shell

>>> from account.models import User
# Normal user
>>> User.objects.create_user(email="...", username="...", password="...")
# Super user
>>> User.objects.create_superuser(email="...", username="...", password="...")
```

