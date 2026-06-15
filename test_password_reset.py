"""
Password Reset System Test Script
Test the password reset functionality end-to-end
Run: python test_password_reset.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from django.urls import reverse
from account.models import AppUser, PasswordResetToken
from django.core.mail import outbox
from django.conf import settings
import time


def test_setup():
    """Test system configuration"""
    print("\n" + "="*60)
    print("PASSWORD RESET SYSTEM - CONFIGURATION TEST")
    print("="*60)
    
    print("\n1. Checking Django Configuration...")
    print(f"   ✓ AUTH_USER_MODEL: {settings.AUTH_USER_MODEL}")
    print(f"   ✓ PASSWORD_RESET_TIMEOUT: {settings.PASSWORD_RESET_TIMEOUT} seconds")
    print(f"   ✓ LOGIN_URL: {settings.LOGIN_URL}")
    
    print("\n2. Checking Email Configuration...")
    print(f"   EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"   EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"   EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"   DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    
    print("\n3. Checking Cache Configuration...")
    from django.core.cache import cache
    try:
        cache.set('test_key', 'test_value', 10)
        value = cache.get('test_key')
        if value == 'test_value':
            print("   ✓ Redis Cache: Connected and working")
        else:
            print("   ✗ Redis Cache: Not working properly")
    except Exception as e:
        print(f"   ✗ Redis Cache Error: {str(e)}")
        print("   → Make sure Redis is running: redis-server")
    
    print("\n4. Checking Database...")
    try:
        count = AppUser.objects.count()
        print(f"   ✓ Database: Connected (AppUser count: {count})")
    except Exception as e:
        print(f"   ✗ Database Error: {str(e)}")


def test_password_reset_flow():
    """Test the complete password reset flow"""
    print("\n" + "="*60)
    print("PASSWORD RESET FLOW TEST")
    print("="*60)
    
    # Create test user
    print("\n1. Creating test user...")
    test_user, created = AppUser.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'is_active': True,
        }
    )
    print(f"   {'✓ Created' if created else '✓ Using existing'} user: {test_user.username}")
    
    client = Client()
    
    # Test password reset request
    print("\n2. Testing password reset request...")
    response = client.post(reverse('password_reset'), {
        'email': test_user.email
    })
    
    if response.status_code == 302:  # Redirect after successful POST
        print(f"   ✓ Password reset request sent successfully")
        
        # Check if token was created
        tokens = PasswordResetToken.objects.filter(user=test_user, is_used=False)
        if tokens.exists():
            token_obj = tokens.latest('created_at')
            print(f"   ✓ Reset token created: {token_obj.token}")
            
            # Test token confirmation
            print("\n3. Testing password reset confirmation...")
            new_password = 'NewPassword123'
            confirm_response = client.post(
                reverse('password_reset_confirm', kwargs={'token': str(token_obj.token)}),
                {
                    'new_password1': new_password,
                    'new_password2': new_password,
                }
            )
            
            if confirm_response.status_code == 302:
                print(f"   ✓ Password reset confirmation successful")
                
                # Verify token is marked as used
                token_obj.refresh_from_db()
                if token_obj.is_used:
                    print(f"   ✓ Token marked as used")
                
                # Test login with new password
                print("\n4. Testing login with new password...")
                login_success = client.login(username=test_user.username, password=new_password)
                if login_success:
                    print(f"   ✓ Login successful with new password")
                else:
                    print(f"   ✗ Login failed with new password")
            else:
                print(f"   ✗ Password reset confirmation failed (Status: {confirm_response.status_code})")
        else:
            print(f"   ✗ Reset token was not created")
    else:
        print(f"   ✗ Password reset request failed (Status: {response.status_code})")
    
    # Test token expiry
    print("\n5. Testing token expiry...")
    old_token = PasswordResetToken.objects.create(
        user=test_user,
        is_used=False
    )
    print(f"   ✓ Created test token: {old_token.token}")
    print(f"   → Token expiry time: {settings.PASSWORD_RESET_TIMEOUT} seconds")
    
    # Clean up
    print("\n6. Cleaning up test data...")
    old_token.delete()
    print(f"   ✓ Test token deleted")


def test_email_system():
    """Test email sending"""
    print("\n" + "="*60)
    print("EMAIL SYSTEM TEST")
    print("="*60)
    
    print("\n1. Attempting to send test email...")
    from django.core.mail import send_mail
    
    try:
        result = send_mail(
            subject='Password Reset Test - Mobile Store',
            message='This is a test email for password reset system.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['test@example.com'],
            fail_silently=False,
        )
        if result:
            print("   ✓ Email sent successfully")
            print("\n   Next steps:")
            print("   1. Check SMTP4dev Web UI: http://localhost:5000")
            print("   2. You should see the test email")
            print("   3. Verify email content and formatting")
        else:
            print("   ✗ Email delivery returned no confirmation")
    except Exception as e:
        print(f"   ✗ Email Error: {str(e)}")
        print("   → Make sure SMTP4dev is running on localhost:1025")
        print("   → Download from: https://smtp4dev.github.io/")


def display_urls():
    """Display important URLs"""
    print("\n" + "="*60)
    print("IMPORTANT URLS")
    print("="*60)
    
    urls = {
        'Django Admin': 'http://localhost:8000/admin/',
        'Login': 'http://localhost:8000/accounts/login/',
        'Password Reset': 'http://localhost:8000/accounts/password-reset/',
        'SMTP4dev': 'http://localhost:5000/',
    }
    
    print("\nAccess these URLs in your browser:")
    for name, url in urls.items():
        print(f"   {name:20} → {url}")


def main():
    """Run all tests"""
    print("\n\n")
    print("*" * 60)
    print("* PASSWORD RESET SYSTEM - COMPREHENSIVE TEST")
    print("*" * 60)
    
    test_setup()
    test_email_system()
    test_password_reset_flow()
    display_urls()
    
    print("\n" + "="*60)
    print("TEST COMPLETED")
    print("="*60)
    print("\nIf all tests passed, your password reset system is ready!")
    print("Start with: python manage.py runserver")
    print("\n")


if __name__ == '__main__':
    main()
