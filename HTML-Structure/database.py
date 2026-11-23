"""
Database initialization and realistic seeder script.
Populates standard roles, test accounts, and audit history.
"""
from datetime import datetime, timezone, timedelta
from models import db, User, AuditLog

def seed_database():
    """Populate default users and activity logs if database is empty."""
    if User.query.first():
        return  # Database already seeded

    now = datetime.now(timezone.utc)

    # 1. Admin Account
    admin = User(
        username="admin",
        email="admin@cognify.com",
        full_name="System Administrator",
        role="admin",
        status="active",
        bio="Lead system administrator overseeing HTML semantic standards, SSR performance, and user access policies.",
        phone="+1 (555) 019-2834",
        location="San Francisco, CA",
        avatar="admin-avatar.svg",
        created_at=now - timedelta(days=90),
        last_login=now - timedelta(hours=2)
    )
    admin.set_password("Admin@12345")

    # 2. Manager Account
    manager = User(
        username="alex_manager",
        email="alex.morgan@cognify.com",
        full_name="Alex Morgan",
        role="manager",
        status="active",
        bio="Engineering Manager in charge of frontend accessibility, semantic markup compliance, and team workflows.",
        phone="+1 (555) 014-9912",
        location="Austin, TX",
        avatar="alex-avatar.svg",
        created_at=now - timedelta(days=60),
        last_login=now - timedelta(days=1)
    )
    manager.set_password("Manager@12345")

    # 3. Regular Active User
    user1 = User(
        username="sarah_dev",
        email="sarah.chen@example.com",
        full_name="Sarah Chen",
        role="user",
        status="active",
        bio="Full-Stack Developer passionate about HTML5 semantic document architecture, web forms, and WCAG accessibility.",
        phone="+1 (555) 018-7731",
        location="Seattle, WA",
        avatar="sarah-avatar.svg",
        created_at=now - timedelta(days=30),
        last_login=now - timedelta(hours=5)
    )
    user1.set_password("User@12345")

    # 4. Another Regular User (Pending)
    user2 = User(
        username="david_k",
        email="david.kumar@example.com",
        full_name="David Kumar",
        role="user",
        status="pending",
        bio="Junior Developer exploring Python server-side rendering pipelines and responsive layouts.",
        phone="+1 (555) 012-4488",
        location="Boston, MA",
        avatar="david-avatar.svg",
        created_at=now - timedelta(days=5),
        last_login=None
    )
    user2.set_password("User@12345")

    # 5. Suspended User (Demonstrating status management)
    user3 = User(
        username="elena_rostova",
        email="elena.r@example.com",
        full_name="Elena Rostova",
        role="user",
        status="suspended",
        bio="Account currently suspended due to security review.",
        phone="+1 (555) 016-3320",
        location="Chicago, IL",
        avatar="elena-avatar.svg",
        created_at=now - timedelta(days=45),
        last_login=now - timedelta(days=12)
    )
    user3.set_password("User@12345")

    db.session.add_all([admin, manager, user1, user2, user3])
    db.session.commit()

    # Add initial audit history
    logs = [
        AuditLog(
            user_id=admin.id,
            action="SYSTEM_INIT",
            details="System initialized with baseline security policies and initial schema.",
            ip_address="127.0.0.1",
            timestamp=now - timedelta(days=90)
        ),
        AuditLog(
            user_id=admin.id,
            action="USER_CREATE",
            details="Created manager account for alex_manager with elevated permissions.",
            ip_address="127.0.0.1",
            timestamp=now - timedelta(days=60)
        ),
        AuditLog(
            user_id=user1.id,
            action="USER_REGISTER",
            details="User sarah_dev completed self-service registration and email verification.",
            ip_address="192.168.1.42",
            timestamp=now - timedelta(days=30)
        ),
        AuditLog(
            user_id=admin.id,
            action="STATUS_SUSPEND",
            details="Suspended user elena_rostova following multiple failed authentication attempts.",
            ip_address="127.0.0.1",
            timestamp=now - timedelta(days=12)
        ),
        AuditLog(
            user_id=admin.id,
            action="ADMIN_LOGIN",
            details="Admin session authenticated successfully.",
            ip_address="127.0.0.1",
            timestamp=now - timedelta(hours=2)
        )
    ]

    db.session.add_all(logs)
    db.session.commit()
    print(">> Database seeded successfully with initial users and audit history.")
