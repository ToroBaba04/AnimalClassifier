# Security Features Implementation Guide

## Overview
Your Animal Classifier app now has comprehensive security features including user authentication, 2FA, and per-user data isolation.

## Features Implemented

### 1. **User Management**
- ✅ User registration with email validation
- ✅ Secure password storage (Django default)
- ✅ User login with email or username support
- ✅ User logout functionality
- ✅ User profile system (UserProfile model)

### 2. **2-Factor Authentication (2FA)**
- ✅ Email-based 2FA codes (6-digit)
- ✅ 2FA required on signup (email verification)
- ✅ 2FA required on login (security verification)
- ✅ 15-minute token expiration
- ✅ One-time use codes (prevents replay attacks)
- ✅ Automatic cleanup of expired tokens

### 3. **Data Privacy & Encryption**
- ✅ Classifications linked to users
- ✅ Users can only see their own predictions
- ✅ User-friendly image paths with date organization
- ✅ Login required for all classification features

### 4. **Security Best Practices**
- ✅ CSRF protection enabled
- ✅ Session security configured
- ✅ Password validation rules applied
- ✅ Secure password hashing (PBKDF2)
- ✅ HTTPOnly cookies
- ✅ User isolation on history page

---

## Setup Instructions

### Step 1: Install New Dependencies
```bash
pip install -r requirements.txt
```

New packages added:
- `django-crispy-forms==2.1` - Better form rendering
- `crispy-bootstrap5==0.7` - Bootstrap 5 styling for forms

### Step 2: Configure Email (Important for 2FA)

Edit `malla/settings.py` and configure your email provider:

**Option A: Gmail (Recommended for testing)**
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # Use app password, not regular password
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

To get Gmail app password:
1. Go to https://myaccount.google.com/security
2. Enable 2-Step Verification
3. Generate "App passwords"
4. Select "Mail" and "Windows Computer"
5. Copy the 16-character password

**Option B: Console Email (Development/Testing)**
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```
Codes will be printed to terminal instead of emailed.

### Step 3: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### Step 5: Run Server
```bash
python manage.py runserver
```

---

## New URLs

```
/register/                 - User registration
/verify-signup-2fa/       - Signup 2FA verification
/login/                    - User login
/verify-login-2fa/        - Login 2FA verification
/logout/                   - User logout
/                          - Main classifier (requires login)
/upload/                   - Image upload API (requires login)
/history/                  - View your predictions (requires login)
```

---

## Database Changes

### New Models:

**UserProfile**
- Links to Django User model
- Stores 2FA settings
- Tracks 2FA verification status

**TwoFactorToken**
- Stores temporary 2FA codes
- Tracks token purpose (signup/login)
- Automatic expiration handling

**Classification** (Updated)
- Added `user` ForeignKey
- Now filtered by logged-in user
- Images organized by date

---

## Testing the System

### Test User Registration:
1. Go to `/register/`
2. Create account with email
3. Check email/console for 6-digit code
4. Enter code on verification page
5. Automatically logged in on success

### Test User Login:
1. Go to `/login/`
2. Enter username/email and password
3. Check email/console for 6-digit code
4. Enter code on verification page
5. Access classifier features

### Test Data Privacy:
1. Create two user accounts
2. Each user uploads images
3. Go to `/history/`
4. You only see YOUR predictions
5. Login as other user to verify isolation

---

## Security Configuration Tips

### Production Deployment:
```python
# In settings.py for production:
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
```

### Email Provider Recommendations:
- **Gmail**: Good for small scale
- **SendGrid**: Good for production
- **mailgun**: Good for transactional mail
- **AWS SES**: Scalable solution

### Additional Security:
- Use environment variables for secrets
- Enable HTTPS in production
- Set strong secret key
- Regular password policy enforcement
- Monitor failed login attempts

---

## File Changes Summary

### Created Files:
- `classifier/models.py` - Added UserProfile, TwoFactorToken models
- `classifier/forms.py` - Added registration, login, 2FA forms
- `classifier/views.py` - Complete authentication system
- `classifier/urls.py` - New authentication routes
- `malla/settings.py` - Email and security configuration
- `classifier/templates/base.html` - Base template with navbar
- `classifier/templates/classifier/register.html` - Registration page
- `classifier/templates/classifier/login.html` - Login page
- `classifier/templates/classifier/verify_2fa.html` - 2FA verification

### Updated Files:
- `requirements.txt` - Added crispy-forms packages
- `classifier/views.py` - Enhanced with authentication
- `classifier/urls.py` - Added auth routes

---

## Troubleshooting

### "Email not sending"
- Check EMAIL settings in settings.py
- Try console backend first: `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'`
- Check Gmail app password format

### "Migrations error"
```bash
python manage.py makemigrations classifier
python manage.py migrate classifier
```

### "400 Bad Request on forms"
- Ensure `{% csrf_token %}` is in all forms
- Check that POST method is used

### "Users can see other users' predictions"
- Verify Classification model has user FK
- Check history view filters by `user=request.user`

---

## Next Steps

1. ✅ Install dependencies
2. ✅ Configure email provider
3. ✅ Run migrations
4. ✅ Test registration/login/2FA flow
5. ✅ Test data privacy isolation
6. ✅ Update index.html to extend base.html
7. ✅ Update history.html to extend base.html
8. Consider adding:
   - Password reset functionality
   - Email change functionality
   - 2FA disable/enable per user
   - Login attempt logging
   - Rate limiting on failed attempts

---

## Support

If you encounter issues:
1. Check Django logs: `python manage.py runserver`
2. Check email configuration in settings.py
3. Verify database migrations: `python manage.py showmigrations`
4. Test email setup: `python manage.py shell` then `from django.core.mail import send_mail`
