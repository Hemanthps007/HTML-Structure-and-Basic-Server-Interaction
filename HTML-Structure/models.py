"""
Database Models for User Management System
Demonstrates structured data models backing Server-Side Rendered (SSR) views.
Includes explicit __init__ definitions for strict static analysis and IDE type safety.
"""
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False)  # 'admin', 'manager', 'user'
    status = db.Column(db.String(20), default='active', nullable=False)  # 'active', 'suspended', 'pending'
    bio = db.Column(db.Text, nullable=True)
    phone = db.Column(db.String(30), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    avatar = db.Column(db.String(200), default='avatar-default.svg', nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)

    # Relationships
    logs = db.relationship('AuditLog', backref='user', lazy=True, cascade='all, delete-orphan')

    def __init__(
        self,
        username: str = "",
        email: str = "",
        full_name: str = "",
        role: str = "user",
        status: str = "active",
        bio: Optional[str] = None,
        phone: Optional[str] = None,
        location: Optional[str] = None,
        avatar: str = "avatar-default.svg",
        created_at: Optional[datetime] = None,
        last_login: Optional[datetime] = None,
        **kwargs: Any
    ):
        super().__init__(**kwargs)
        self.username = username
        self.email = email
        self.full_name = full_name
        self.role = role
        self.status = status
        self.bio = bio
        self.phone = phone
        self.location = location
        self.avatar = avatar
        if created_at is not None:
            self.created_at = created_at
        if last_login is not None:
            self.last_login = last_login

    def set_password(self, password: str):
        """Hash and store user password using secure scrypt/pbkdf2."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verify plain password against stored hash."""
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self) -> bool:
        return self.role == 'admin'

    @property
    def is_manager(self) -> bool:
        return self.role in ('admin', 'manager')

    @property
    def is_active(self) -> bool:
        return self.status == 'active'

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'role': self.role,
            'status': self.status,
            'bio': self.bio,
            'phone': self.phone,
            'location': self.location,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'last_login': self.last_login.strftime('%Y-%m-%d %H:%M:%S') if self.last_login else 'Never'
        }


class AuditLog(db.Model):
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    action = db.Column(db.String(80), nullable=False, index=True)
    details = db.Column(db.Text, nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)

    def __init__(
        self,
        user_id: Optional[int] = None,
        action: str = "",
        details: Optional[str] = None,
        ip_address: Optional[str] = None,
        timestamp: Optional[datetime] = None,
        **kwargs: Any
    ):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.action = action
        self.details = details
        self.ip_address = ip_address
        if timestamp is not None:
            self.timestamp = timestamp

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.user.username if self.user else 'System',
            'action': self.action,
            'details': self.details,
            'ip_address': self.ip_address,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
