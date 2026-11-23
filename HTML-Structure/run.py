"""
Main entrypoint runner for the HTML Structure User Management Application.
Runs the Flask Server-Side Rendering (SSR) server on localhost.
"""
import sys
from app import app

if __name__ == '__main__':
    port = 5000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass

    print("=" * 68)
    print(" 🚀 Cognify HTML-Structure & SSR User Management System")
    print("=" * 68)
    print(f" * Server running on: http://127.0.0.1:{port}")
    print(" * Pre-configured Accounts:")
    print("   - Administrator: admin / Admin@12345 (Role: Admin)")
    print("   - Manager:       alex_manager / Manager@12345 (Role: Manager)")
    print("   - Member:        sarah_dev / User@12345 (Role: User)")
    print(" * Educational HTML Structure Guide: http://127.0.0.1:{port}/html-guide")
    print("=" * 68)

    app.run(host='127.0.0.1', port=port, debug=True)
