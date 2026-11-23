"""
Automated Test Suite for HTML-Structure & SSR User Management System.
Validates routes, SSR compilation, semantic markup presence, authentication, and RBAC policies.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import unittest
from app import app, db
from models import User, AuditLog

class UserManagementSSRTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()

        with app.app_context():
            db.create_all()
            from database import seed_database
            seed_database()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_01_public_routes_status_and_semantics(self):
        """Test landing page, guide, login, and registration return 200 and have semantic HTML5 landmarks."""
        for path in ['/', '/html-guide', '/login', '/register', '/reset-password']:
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200, f"Route {path} failed with {response.status_code}")
            html = response.data.decode('utf-8')
            # Check for critical HTML5 document elements & landmarks
            self.assertIn('<!DOCTYPE html>', html)
            self.assertIn('<html lang="en"', html)
            self.assertIn('<header class="site-header" role="banner">', html)
            self.assertIn('<main id="main-content" class="site-main" role="main">', html)
            self.assertIn('<footer class="site-footer" role="contentinfo">', html)

    def test_02_form_semantic_structure(self):
        """Verify registration and login pages include fieldsets, legends, and explicit labels."""
        reg_response = self.client.get('/register')
        reg_html = reg_response.data.decode('utf-8')
        self.assertIn('<fieldset', reg_html)
        self.assertIn('<legend', reg_html)
        self.assertIn('<label for="username"', reg_html)
        self.assertIn('<input', reg_html)

        login_response = self.client.get('/login')
        login_html = login_response.data.decode('utf-8')
        self.assertIn('<fieldset', login_html)
        self.assertIn('<legend', login_html)
        self.assertIn('<label for="identifier"', login_html)

    def test_03_login_authentication_and_session(self):
        """Test user login, session cookie generation, and profile redirection."""
        response = self.client.post('/login', data={
            'identifier': 'sarah_dev',
            'password': 'User@12345'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn('Welcome back, Sarah Chen!', html)
        self.assertIn('sarah.chen@example.com', html)

    def test_04_rbac_access_restrictions(self):
        """Test that regular users cannot access administrative endpoints (403 Forbidden)."""
        # 1. Login as standard user
        self.client.post('/login', data={'identifier': 'sarah_dev', 'password': 'User@12345'})
        
        # 2. Attempt admin dashboard access -> Expect 403 Forbidden
        response = self.client.get('/admin/dashboard')
        self.assertEqual(response.status_code, 403)
        html = response.data.decode('utf-8')
        self.assertIn('403', html)
        self.assertIn('Access Forbidden', html)

        # 3. Attempt admin users directory access -> Expect 403 Forbidden
        response = self.client.get('/admin/users')
        self.assertEqual(response.status_code, 403)

    def test_05_admin_authenticated_access(self):
        """Test that administrator can access dashboard, directory table, and audit trail."""
        # Login as admin
        self.client.post('/login', data={'identifier': 'admin', 'password': 'Admin@12345'})

        # Admin Dashboard
        resp_dash = self.client.get('/admin/dashboard')
        self.assertEqual(resp_dash.status_code, 200)
        self.assertIn('Administrative Dashboard', resp_dash.data.decode('utf-8'))

        # Admin User Directory Table
        resp_users = self.client.get('/admin/users')
        self.assertEqual(resp_users.status_code, 200)
        users_html = resp_users.data.decode('utf-8')
        self.assertIn('<table', users_html)
        self.assertIn('Registered Users', users_html)
        self.assertIn('admin@cognify.com', users_html)

        # Audit Logs
        resp_logs = self.client.get('/admin/audit-logs')
        self.assertEqual(resp_logs.status_code, 200)
        self.assertIn('System Audit Trail', resp_logs.data.decode('utf-8'))

    def test_06_user_registration_flow(self):
        """Test self-service registration with validation and auto-login."""
        response = self.client.post('/register', data={
            'full_name': 'Marcus Aurelius',
            'username': 'marcus_a',
            'email': 'marcus@example.com',
            'password': 'Password@123',
            'confirm_password': 'Password@123',
            'terms': 'on'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn('Marcus Aurelius', html)

        with app.app_context():
            new_user = User.query.filter_by(username='marcus_a').first()
            self.assertIsNotNone(new_user)
            self.assertEqual(new_user.email, 'marcus@example.com')

    def test_07_error_404_handling(self):
        """Test semantic 404 page rendering for non-existent routes."""
        response = self.client.get('/non-existent-page-url-xyz')
        self.assertEqual(response.status_code, 404)
        html = response.data.decode('utf-8')
        self.assertIn('404', html)
        self.assertIn('Page Not Found', html)

if __name__ == '__main__':
    unittest.main(verbosity=2)
