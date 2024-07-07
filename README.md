# Food Management System

> [Client Repository](https://github.com/VishnuKumarSS/Food-Management-System-ReactJS-FE)

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

# Verify OTP (Ignore this, Instead use Login User / Token Obtain API)
API Method: POST
API Endpoint: {{BASE_URL_BE}}/account/verify-otp/
Body:
{
    "email": "USER_EMAIL",
    "otp": "RECEIVED OTP"
}

```

#### 3. Authentication APIs
```bash
# Create/Register User
API Method: POST
API Endpoint: {{BASE_URL_BE}}/account/register/
Body:
{
    "username": "username",
    "email": "useremail@gmail.com",
    "password": "password"
}

# Login User / Token Obtain
API Method: POST
API Endpoint: {{BASE_URL_BE}}/account/token/
Body:
{
    "email": "useremail@gmail.com",
    "otp": "123456", # Required for the first time
    "password": "password"
}

# Token refresh
API Method: POST
API Endpoint: {{BASE_URL_BE}}/account/token/refresh/
Body:
{
    "refresh": "headers.payload.signature"
}
```

#### 4. Access user details
```bash
API Method: GET
API Endpoint: {{BASE_URL_BE}}/account/userdata/
Headers:
key: Authorization
value: Bearer <access token>

Sample Response:
{
    "uid": "userid",
    "username": "username",
    "email": "useremail@gmail.com",
    "is_email_verified": true,
    "is_admin": false,
    "is_superuser": false,
    "is_active": true,
    "created_at": "2024-06-15T19:57:11.936165Z",
    "updated_at": "2024-06-16T11:53:10.238012Z"
}
```
