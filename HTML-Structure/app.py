"""
Flask Server-Side Rendering (SSR) Application
Demonstrates complete HTML Document Structure, Semantic Tags, and Full-Featured User Management.
"""
import os
import sys

# Ensure current directory is in sys.path for IDE language servers & runtime execution
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timezone
from functools import wraps
from flask import (
    Flask, render_template, request, redirect, url_for,
    flash, session, g, abort, has_request_context
)

try:
    from models import db, User, AuditLog
    from database import seed_database
    from forms import validate_registration, validate_profile_update
except ImportError:
    from .models import db, User, AuditLog
    from .database import seed_database
    from .forms import validate_registration, validate_profile_update

# Initialize application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'cognify-html-structure-secure-session-key-2026')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usermanagement.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# -------------------------------------------------------------------------
# Authentication & Access Control Decorators
# -------------------------------------------------------------------------
@app.before_request
def load_current_user():
    """Load logged-in user into Flask's `g` context before each request."""
    user_id = session.get('user_id')
    if user_id:
        g.user = db.session.get(User, user_id)
    else:
        g.user = None

@app.context_processor
def inject_global_template_vars():
    """Inject current_user, year, and app metadata into all Jinja2 SSR templates."""
    return {
        'current_user': g.user,
        'current_year': datetime.now().year,
        'app_name': 'Cognify User Management',
        'is_authenticated': g.user is not None
    }

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            flash("Please sign in to access this page.", "warning")
            return redirect(url_for('login', next=request.path))
        if g.user.status == 'suspended':
            session.clear()
            flash("Your account is currently suspended. Please contact an administrator.", "danger")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def manager_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            flash("Please sign in to access this page.", "warning")
            return redirect(url_for('login', next=request.path))
        if not g.user.is_manager:
            flash("Access forbidden: Manager or Admin privileges required.", "danger")
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            flash("Please sign in to access this page.", "warning")
            return redirect(url_for('login', next=request.path))
        if not g.user.is_admin:
            flash("Access forbidden: Administrator privileges required.", "danger")
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def log_action(user_id, action, details):
    """Record an audit trail event."""
    try:
        ip = '127.0.0.1'
        if has_request_context():
            ip = request.remote_addr or '127.0.0.1'
        log = AuditLog(
            user_id=user_id,
            action=action,
            details=details,
            ip_address=ip
        )
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Failed to log audit action: {e}")

# -------------------------------------------------------------------------
# Public & Informational Routes
# -------------------------------------------------------------------------
@app.route('/')
def index():
    """Landing page: Highlights HTML structure architecture and system statistics."""
    total_users = User.query.count()
    active_users = User.query.filter_by(status='active').count()
    total_logs = AuditLog.query.count()
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()

    return render_template(
        'index.html',
        total_users=total_users,
        active_users=active_users,
        total_logs=total_logs,
        recent_users=recent_users
    )

@app.route('/html-guide')
def html_guide():
    """Educational walkthrough explaining semantic HTML5 structure used in the project."""
    return render_template('html_guide.html')

# -------------------------------------------------------------------------
# Authentication Routes
# -------------------------------------------------------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    """Self-service registration with accessible form structure."""
    if g.user:
        return redirect(url_for('profile'))

    errors = {}
    form_data = {}

    if request.method == 'POST':
        form_data = request.form.to_dict()
        existing_usernames = [u.username for u in User.query.with_entities(User.username).all()]
        existing_emails = [u.email for u in User.query.with_entities(User.email).all()]

        errors, sanitized = validate_registration(form_data, existing_usernames, existing_emails)

        if not errors:
            new_user = User(
                username=sanitized['username'],
                email=sanitized['email'],
                full_name=sanitized['full_name'],
                role='user',
                status='active',
                avatar='avatar-default.svg'
            )
            new_user.set_password(form_data.get('password'))
            db.session.add(new_user)
            db.session.commit()

            log_action(new_user.id, "USER_REGISTER", f"Account created for {new_user.username}")

            session['user_id'] = new_user.id
            flash(f"Welcome to Cognify, {new_user.full_name}! Your account has been created successfully.", "success")
            return redirect(url_for('profile'))

    return render_template('auth/register.html', errors=errors, form_data=form_data)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login with validation and session creation."""
    if g.user:
        return redirect(url_for('profile'))

    next_url = request.args.get('next', '')
    errors = {}
    form_data = {}

    if request.method == 'POST':
        identifier = request.form.get('identifier', '').strip()
        password = request.form.get('password', '')
        remember = bool(request.form.get('remember'))
        next_url = request.form.get('next_url', '')

        form_data['identifier'] = identifier

        if not identifier:
            errors['identifier'] = "Please enter your username or email address."
        if not password:
            errors['password'] = "Please enter your password."

        if not errors:
            user = User.query.filter(
                (User.username == identifier) | (User.email == identifier.lower())
            ).first()

            if user and user.check_password(password):
                if user.status == 'suspended':
                    flash("Your account has been suspended by an administrator.", "danger")
                    return render_template('auth/login.html', errors={'auth': "Account suspended."}, form_data=form_data, next_url=next_url)

                session['user_id'] = user.id
                if remember:
                    session.permanent = True

                user.last_login = datetime.now(timezone.utc)
                db.session.commit()

                log_action(user.id, "USER_LOGIN", f"Successful login from IP {request.remote_addr or '127.0.0.1'}")
                flash(f"Welcome back, {user.full_name}!", "success")

                if next_url and next_url.startswith('/'):
                    return redirect(next_url)
                return redirect(url_for('profile'))
            else:
                errors['auth'] = "Invalid username/email or password."

    return render_template('auth/login.html', errors=errors, form_data=form_data, next_url=next_url)


@app.route('/logout')
def logout():
    """Logout current user and terminate session."""
    if g.user:
        log_action(g.user.id, "USER_LOGOUT", "User logged out successfully.")
    session.clear()
    flash("You have been signed out successfully.", "info")
    return redirect(url_for('login'))


@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    """Password recovery simulation."""
    message = None
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        user = User.query.filter_by(email=email).first()
        if user:
            # Simulated token generation
            log_action(user.id, "PASSWORD_RESET_REQ", "Password reset request initiated.")
            message = f"Password reset instructions have been generated for {email}. (Demo: Temporary code is 884-219)"
        else:
            message = "If an account exists with that email, instructions have been dispatched."

    return render_template('auth/reset_password.html', message=message)

# -------------------------------------------------------------------------
# User Profile Management
# -------------------------------------------------------------------------
@app.route('/profile')
@login_required
def profile():
    """Display user profile using semantic HTML structure."""
    user_logs = AuditLog.query.filter_by(user_id=g.user.id).order_by(AuditLog.timestamp.desc()).limit(8).all()
    return render_template('profile/view.html', user=g.user, user_logs=user_logs)


@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Edit personal profile details."""
    errors = {}
    form_data = {
        'full_name': g.user.full_name,
        'email': g.user.email,
        'phone': g.user.phone or '',
        'location': g.user.location or '',
        'bio': g.user.bio or '',
        'avatar': g.user.avatar
    }

    if request.method == 'POST':
        existing_emails = [
            u.email for u in User.query.filter(User.id != g.user.id).with_entities(User.email).all()
        ]
        errors, sanitized = validate_profile_update(request.form.to_dict(), g.user.id, existing_emails)

        avatar_choice = request.form.get('avatar', g.user.avatar)

        if not errors:
            g.user.full_name = sanitized['full_name']
            g.user.email = sanitized['email']
            g.user.phone = sanitized['phone']
            g.user.location = sanitized['location']
            g.user.bio = sanitized['bio']
            g.user.avatar = avatar_choice

            db.session.commit()
            log_action(g.user.id, "PROFILE_UPDATE", "User updated personal profile details.")
            flash("Your profile information has been successfully updated.", "success")
            return redirect(url_for('profile'))
        else:
            form_data = request.form.to_dict()

    return render_template('profile/edit.html', errors=errors, form_data=form_data)


@app.route('/profile/change-password', methods=['POST'])
@login_required
def change_password():
    """Update current user password."""
    current_pwd = request.form.get('current_password', '')
    new_pwd = request.form.get('new_password', '')
    confirm_pwd = request.form.get('confirm_password', '')

    if not g.user.check_password(current_pwd):
        flash("The current password entered is incorrect.", "danger")
        return redirect(url_for('edit_profile'))

    if len(new_pwd) < 8:
        flash("New password must be at least 8 characters long.", "danger")
        return redirect(url_for('edit_profile'))

    if new_pwd != confirm_pwd:
        flash("New passwords do not match.", "danger")
        return redirect(url_for('edit_profile'))

    g.user.set_password(new_pwd)
    db.session.commit()
    log_action(g.user.id, "PASSWORD_CHANGE", "User successfully modified password.")
    flash("Password updated successfully.", "success")
    return redirect(url_for('profile'))

# -------------------------------------------------------------------------
# Admin & Manager Access Control (RBAC)
# -------------------------------------------------------------------------
@app.route('/admin/dashboard')
@manager_required
def admin_dashboard():
    """Administrative overview and analytics."""
    total_users = User.query.count()
    active_count = User.query.filter_by(status='active').count()
    pending_count = User.query.filter_by(status='pending').count()
    suspended_count = User.query.filter_by(status='suspended').count()
    admin_count = User.query.filter_by(role='admin').count()
    manager_count = User.query.filter_by(role='manager').count()
    regular_count = User.query.filter_by(role='user').count()

    recent_logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(10).all()
    recent_users = User.query.order_by(User.created_at.desc()).limit(6).all()

    return render_template(
        'admin/dashboard.html',
        total_users=total_users,
        active_count=active_count,
        pending_count=pending_count,
        suspended_count=suspended_count,
        admin_count=admin_count,
        manager_count=manager_count,
        regular_count=regular_count,
        recent_logs=recent_logs,
        recent_users=recent_users
    )


@app.route('/admin/users')
@manager_required
def admin_users():
    """Searchable, filterable, paginated user management table."""
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('q', '').strip()
    role_filter = request.args.get('role', '').strip()
    status_filter = request.args.get('status', '').strip()

    query = User.query

    if search_query:
        query = query.filter(
            (User.username.ilike(f'%{search_query}%')) |
            (User.email.ilike(f'%{search_query}%')) |
            (User.full_name.ilike(f'%{search_query}%'))
        )

    if role_filter and role_filter in ['admin', 'manager', 'user']:
        query = query.filter_by(role=role_filter)

    if status_filter and status_filter in ['active', 'suspended', 'pending']:
        query = query.filter_by(status=status_filter)

    pagination = query.order_by(User.created_at.desc()).paginate(page=page, per_page=6, error_out=False)

    return render_template(
        'admin/users.html',
        pagination=pagination,
        users=pagination.items,
        search_query=search_query,
        role_filter=role_filter,
        status_filter=status_filter
    )


@app.route('/admin/users/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_edit_user(user_id):
    """Admin route to alter role and status of a user."""
    target_user = db.session.get(User, user_id)
    if not target_user:
        flash("User not found.", "warning")
        return redirect(url_for('admin_users'))

    if request.method == 'POST':
        new_role = request.form.get('role')
        new_status = request.form.get('status')
        new_name = request.form.get('full_name', '').strip()

        if new_role in ['admin', 'manager', 'user']:
            target_user.role = new_role
        if new_status in ['active', 'suspended', 'pending']:
            target_user.status = new_status
        if new_name:
            target_user.full_name = new_name

        db.session.commit()
        log_action(g.user.id, "ADMIN_USER_MOD", f"Updated user #{target_user.id} ({target_user.username}) -> Role: {new_role}, Status: {new_status}")
        flash(f"User {target_user.username} has been updated.", "success")
        return redirect(url_for('admin_users'))

    return render_template('admin/user_edit.html', target_user=target_user)


@app.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def admin_delete_user(user_id):
    """Admin route to remove user account."""
    if g.user.id == user_id:
        flash("You cannot delete your own administrator account.", "danger")
        return redirect(url_for('admin_users'))

    target_user = db.session.get(User, user_id)
    if not target_user:
        flash("User not found.", "warning")
        return redirect(url_for('admin_users'))

    username = target_user.username
    db.session.delete(target_user)
    db.session.commit()

    log_action(g.user.id, "ADMIN_USER_DELETE", f"Deleted user {username} (ID: {user_id})")
    flash(f"User account '{username}' was permanently deleted.", "success")
    return redirect(url_for('admin_users'))


@app.route('/admin/audit-logs')
@manager_required
def admin_audit_logs():
    """View complete audit logs table."""
    page = request.args.get('page', 1, type=int)
    action_filter = request.args.get('action', '').strip()

    query = AuditLog.query

    if action_filter:
        query = query.filter(AuditLog.action.ilike(f'%{action_filter}%'))

    pagination = query.order_by(AuditLog.timestamp.desc()).paginate(page=page, per_page=12, error_out=False)

    return render_template(
        'admin/audit_logs.html',
        pagination=pagination,
        logs=pagination.items,
        action_filter=action_filter
    )

# -------------------------------------------------------------------------
# Error Handlers
# -------------------------------------------------------------------------
@app.errorhandler(403)
def forbidden_error(error):
    return render_template('errors/403.html'), 403

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

# -------------------------------------------------------------------------
# Application Initialization
# -------------------------------------------------------------------------
with app.app_context():
    db.create_all()
    seed_database()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
