# Password Reset Implementation Guide

## Overview
Complete password reset authentication system with email activation links using Redis caching and SMTP4dev for local email testing.

## Architecture

### Components
1. **PasswordResetToken Model** - Stores reset tokens linked to users
2. **Redis Cache** - For session management and performance
3. **SMTP4dev** - Local email server for development testing
4. **Email Templates** - HTML email with reset link and confirmation pages
5. **Views** - Handle password reset flow
6. **Forms** - Validate email and new password

### Flow Diagram
```
User → Password Reset Page
    ↓
Enter Email → Send Reset Link
    ↓
Email Sent (SMTP4dev) → User clicks link in email
    ↓
Verify Token (check expiry + is_used flag)
    ↓
Set New Password Page
    ↓
Password Updated → Redirect to Success Page
    ↓
User can Login with New Password
```

## Setup Instructions

### 1. Prerequisites
- Redis installed and running on localhost:6379
- SMTP4dev installed and running (default: localhost:1025)
- Django 5.2.14
- Python 3.10+

### 2. Install Required Package
```bash
pip install django-redis
```

### 3. Start Services

**Start Redis:**
```bash
# Windows (if using Redis for Windows)
redis-server

# Or use WSL:
wsl redis-server
```

**Start SMTP4dev:**
```bash
# Download from: https://smtp4dev.github.io/
# Run the executable
smtp4dev.exe
# Web UI available at: http://localhost:5000
```

### 4. Configuration Verification

**settings.py should have:**
```python
# Redis Cache
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = 'noreply@mobilestore.com'

# Password Reset
PASSWORD_RESET_TIMEOUT = 3600  # 1 hour
```

### 5. Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## URL Routes

| Route | View | Purpose |
|-------|------|---------|
| `/accounts/password-reset/` | PasswordResetView | Request password reset |
| `/accounts/password-reset-done/` | PasswordResetDoneView | Confirmation after email sent |
| `/accounts/password-reset/<token>/` | PasswordResetConfirmView | Reset password with token |
| `/accounts/password-reset-success/` | PasswordResetSuccessView | Success confirmation |

## Testing the System

### Step 1: Request Password Reset
1. Go to http://localhost:8000/accounts/login/
2. Click "Forgot Password?" link
3. Enter your registered email address
4. Click "Send Reset Link"

### Step 2: Check Email
1. Open SMTP4dev Web UI: http://localhost:5000
2. You should see the password reset email
3. Copy the reset link from the email (or click if link is clickable)

### Step 3: Reset Password
1. Visit the reset link
2. Enter your new password
3. Confirm the new password
4. Click "Update Password"
5. See success message

### Step 4: Login
1. Go to login page
2. Enter username and new password
3. You should login successfully

## Key Features

### 1. Token Management
- Unique UUID tokens generated per reset request
- Old tokens automatically invalidated when new reset requested
- Tokens expire after 1 hour (configurable)
- Tokens marked as used after password update

### 2. Security
- Tokens stored in database (linked to user)
- Email validation - only registered emails can request reset
- One-time use tokens (is_used flag)
- Time-based expiry
- CSRF protection on all forms

### 3. Email System
- HTML email with gradient styling
- Plaintext fallback
- Personalized greeting with user's first name
- Security warnings in email
- Expiry time mentioned (1 hour)

### 4. User Experience
- Clear error messages
- Success confirmations
- Responsive Bootstrap 5 design
- Consistent auth_base template (minimal layout)
- Back links for navigation

## Admin Interface

### View Reset Tokens
1. Go to Django Admin: http://localhost:8000/admin/
2. Navigate to "Password Reset Tokens" section
3. See all reset requests with:
   - User
   - Token (read-only)
   - Created date
   - Used status

### Manage Tokens
- Search by email, username, or token
- Filter by used/unused
- View creation timestamp
- Delete expired tokens (manual cleanup)

## Database Schema

### PasswordResetToken Table
```sql
Column        | Type                | Notes
--------------+---------------------+---------------------------
id            | BigAutoField        | Primary key
user_id       | BigInteger (FK)     | Links to AppUser
token         | CharField(100)      | Unique UUID token
created_at    | DateTimeField       | Auto-created timestamp
is_used       | BooleanField        | Default False
```

## Environment Variables (Optional)

For production, move sensitive configs to environment:
```bash
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

## Troubleshooting

### Issue: Email not sending
**Check:**
1. SMTP4dev is running on localhost:1025
2. Settings.py email config is correct
3. Check SMTP4dev Web UI for errors: http://localhost:5000

### Issue: Token expired too quickly
**Solution:** Increase PASSWORD_RESET_TIMEOUT in settings.py
```python
PASSWORD_RESET_TIMEOUT = 7200  # 2 hours
```

### Issue: Redis connection error
**Check:**
1. Redis is running: `redis-cli ping` should return "PONG"
2. LOCATION in CACHES points to correct Redis instance
3. Redis default port is 6379

### Issue: Template not found
**Verify:**
1. Templates are in `templates/account/` folder
2. BASE_DIR / 'templates' is in TEMPLATES['DIRS']
3. Run `python manage.py check` for template errors

## Customization

### Change Email Sender Name
Update in `account/views.py`:
```python
DEFAULT_FROM_EMAIL = 'support@yourcompany.com'
```

### Change Email Template
Edit `templates/account/password_reset_email.html`

### Change Token Expiry
Update in `settings.py`:
```python
PASSWORD_RESET_TIMEOUT = 1800  # 30 minutes
```

### Change Form Styling
Edit form classes in `account/forms.py`:
```python
widget=forms.EmailInput(attrs={
    'class': 'form-control form-control-lg',  # Add custom classes
    ...
})
```

## Files Modified/Created

### Created:
- `account/forms.py` - Password reset forms
- `account/migrations/0005_passwordresettoken.py` - Database migration
- `templates/account/password_reset.html` - Reset request page
- `templates/account/password_reset_email.html` - Email template
- `templates/account/password_reset_confirm.html` - Reset form page
- `templates/account/password_reset_done.html` - Confirmation page
- `templates/account/password_reset_success.html` - Success page

### Modified:
- `config/settings.py` - Added Redis and email config
- `account/models.py` - Added PasswordResetToken model
- `account/views.py` - Added 4 password reset views
- `account/urls.py` - Added 4 new URL routes
- `account/admin.py` - Registered PasswordResetToken in admin
- `templates/account/login.html` - Added "Forgot Password?" link

## Next Steps

1. ✅ Implement password reset with email activation
2. Optional: Add email verification on signup
3. Optional: Implement 2FA (Two-Factor Authentication)
4. Optional: Add password change for logged-in users
5. Optional: Email digest/notification system

## Production Checklist

- [ ] Change EMAIL_BACKEND to production SMTP provider
- [ ] Move secrets to environment variables
- [ ] Set PASSWORD_RESET_TIMEOUT appropriately (usually 1-2 hours)
- [ ] Enable email templates in production
- [ ] Add logging for password reset attempts
- [ ] Consider rate limiting on password reset endpoint
- [ ] Test email delivery
- [ ] Test token expiry
- [ ] Monitor Redis performance
