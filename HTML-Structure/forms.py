"""
Form validation and sanitation utilities for Server-Side Rendering (SSR).
Ensures data integrity and surfaces accessible validation messages.
"""
import re

def validate_registration(form_data, existing_usernames, existing_emails):
    """Validate user registration inputs."""
    errors = {}

    username = form_data.get('username', '').strip()
    email = form_data.get('email', '').strip().lower()
    full_name = form_data.get('full_name', '').strip()
    password = form_data.get('password', '')
    confirm_password = form_data.get('confirm_password', '')
    terms = form_data.get('terms')

    # Username validation
    if not username:
        errors['username'] = "Username is required."
    elif len(username) < 3 or len(username) > 30:
        errors['username'] = "Username must be between 3 and 30 characters."
    elif not re.match(r'^[a-zA-Z0-9_]+$', username):
        errors['username'] = "Username can only contain letters, numbers, and underscores."
    elif username.lower() in [u.lower() for u in existing_usernames]:
        errors['username'] = "This username is already registered."

    # Email validation
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not email:
        errors['email'] = "Email address is required."
    elif not re.match(email_regex, email):
        errors['email'] = "Please provide a valid email address (e.g., name@example.com)."
    elif email in [e.lower() for e in existing_emails]:
        errors['email'] = "This email is already associated with an account."

    # Full name validation
    if not full_name:
        errors['full_name'] = "Full name is required."
    elif len(full_name) < 2:
        errors['full_name'] = "Full name must be at least 2 characters."

    # Password validation
    if not password:
        errors['password'] = "Password is required."
    elif len(password) < 8:
        errors['password'] = "Password must be at least 8 characters long."
    elif not any(c.isupper() for c in password):
        errors['password'] = "Password must contain at least one uppercase letter."
    elif not any(c.isdigit() for c in password):
        errors['password'] = "Password must contain at least one number."

    # Confirm password validation
    if password != confirm_password:
        errors['confirm_password'] = "Passwords do not match."

    # Terms checkbox
    if not terms:
        errors['terms'] = "You must agree to the Terms of Service and Privacy Policy."

    return errors, {
        'username': username,
        'email': email,
        'full_name': full_name
    }


def validate_profile_update(form_data, current_user_id, existing_emails):
    """Validate profile modifications."""
    errors = {}

    full_name = form_data.get('full_name', '').strip()
    email = form_data.get('email', '').strip().lower()
    phone = form_data.get('phone', '').strip()
    location = form_data.get('location', '').strip()
    bio = form_data.get('bio', '').strip()

    if not full_name:
        errors['full_name'] = "Full name is required."

    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not email:
        errors['email'] = "Email address is required."
    elif not re.match(email_regex, email):
        errors['email'] = "Please enter a valid email address."
    elif email in [e.lower() for e in existing_emails]:
        errors['email'] = "This email address is already in use by another user."

    if bio and len(bio) > 500:
        errors['bio'] = "Bio cannot exceed 500 characters."

    return errors, {
        'full_name': full_name,
        'email': email,
        'phone': phone,
        'location': location,
        'bio': bio
    }
