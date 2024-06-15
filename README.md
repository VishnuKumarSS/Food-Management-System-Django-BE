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

#### 5. EMAIL SMTP server config

Generate the App password in the Google account, and replace the email and 12 digit app password for the below key in .env
```bash
EMAIL_HOST_USER=gmail_host_user_email
EMAIL_HOST_PASSWORD=gmail_host_app_password_12_digit
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

#### 2. Generate and Verify OTP
```bash
# Generate OTP
API Method: POST
API Endpoint: {{BASE_URL_BE}}/account/request-otp/
Body:
{
    "email": "USER_EMAIL"
}

# Verify OTP
API Method: POST
API Endpoint: {{BASE_URL_BE}}/account/verify-otp/
Body:
{
    "email": "USER_EMAIL",
    "otp": "RECEIVED OTP"
}

```