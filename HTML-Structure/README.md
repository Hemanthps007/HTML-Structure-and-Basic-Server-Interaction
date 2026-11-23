# Semantic HTML5 Structure & Server-Side Rendered (SSR) User Management System

A production-grade educational and functional web application engineered to demonstrate the **critical aspects of modern HTML5 document architecture**, **accessible web form design**, and **Server-Side Rendering (SSR)** using **Python**, **Flask**, **Jinja2**, and **SQLite**.

---

## 🌟 Executive Overview

Modern web development frequently suffers from "div soup" and unsemantic markup, creating barriers for screen readers, search engines, and maintainability. This project serves as a comprehensive reference implementation covering:

1. **Semantic HTML5 Document Anatomy**: Complete document hierarchy using standard landmarks (`<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<aside>`, `<footer>`, `<figure>`, `<figcaption>`).
2. **Accessible Form Engineering (WCAG 2.1 AA)**: Multi-fieldset structure, `<legend>` captions, programmatic `<label for="...">` associations, semantic input types (`email`, `password`, `tel`, `checkbox`, `search`), and ARIA error states (`aria-invalid`, `aria-describedby`).
3. **Python Server-Side Rendering (SSR)**: Pure server-side page compilation via Flask and Jinja2 template inheritance, delivering immediate first-paint HTML without client-side hydration lag.
4. **Role-Based Access Control (RBAC)**: Complete multi-role user management (Administrator, Manager, Standard User) with route guards, account status policies (`active`, `pending`, `suspended`), and persistent audit logging.
5. **Interactive Semantic Tag Inspector**: A live visual overlay built directly into the UI that highlights and labels every HTML5 semantic container on any page.

---

## 📂 Project Directory Structure

```
HTML-Structure/
├── app.py                     # Core Flask SSR application, routes, RBAC guards & error handlers
├── models.py                  # SQLAlchemy ORM models (User, AuditLog) & password hashing
├── database.py                # Database initialization & realistic demo data seeder
├── forms.py                   # Server-side validation rules & sanitization routines
├── run.py                     # CLI launcher script with runtime banner & port configuration
├── requirements.txt           # Python dependency specification
├── README.md                  # Comprehensive architectural documentation & run guide
├── static/
│   ├── css/
│   │   ├── style.css          # Design system, CSS variables, typography, forms, tables & responsive grids
│   │   └── html-guide.css     # Educational guide styles & visual Semantic Tag Inspector overlay
│   └── js/
│       └── main.js            # Progressive enhancement: inspector toggle, password reveal, demo auto-fill
└── templates/
    ├── base.html              # Master semantic HTML5 layout skeleton with landmark tags & skip-link
    ├── index.html             # Homepage: metrics, architecture cards, recent users, demo credentials
    ├── html_guide.html        # Comprehensive HTML structure educational handbook & specs
    ├── auth/
    │   ├── login.html         # Accessible login view with one-click demo credentials
    │   ├── register.html      # Multi-fieldset registration view with password requirements
    │   └── reset_password.html# Token-based password recovery simulation
    ├── profile/
    │   ├── view.html          # Profile view: <article>, <figure>, <dl>, <dt>, <dd>, <time>
    │   └── edit.html          # Profile editor: general metadata & password change fieldsets
    ├── admin/
    │   ├── dashboard.html     # Telemetry overview: user counts, health status, audit timeline
    │   ├── users.html         # Searchable, filterable, paginated user management table
    │   ├── user_edit.html     # Administrative role & status modification view
    │   └── audit_logs.html    # Full system audit trail with event filtering
    ├── errors/
    │   ├── 403.html           # 403 Forbidden semantic error view
    │   ├── 404.html           # 404 Not Found semantic error view
    │   └── 500.html           # 500 Internal Server Error semantic view
    └── components/
        ├── alerts.html        # Flash alert messages using <aside role="alert">
        └── pagination.html    # Accessible pagination using <nav aria-label="Pagination">
```

---

## 📐 Critical HTML Structure Concepts Demonstrated

| Semantic Element | Architectural Purpose in this Project | Key Attributes / Accessibility Features |
| :--- | :--- | :--- |
| `<!DOCTYPE html>` | Enforces modern HTML5 standards mode rendering | Avoids browser quirks mode |
| `<html lang="en">` | Establishes root document container and primary language | Enables correct screen reader pronunciation |
| `<header role="banner">` | Global banner housing brand logo and primary navigation | Identifies top-level landmark |
| `<nav aria-label="...">` | Groups major navigation links and submenus | `aria-label="Primary Navigation"` differentiates navbars |
| `<main role="main">` | Encloses central, unique content of the view | Exactly one visible `<main>` per page; keyboard skip-target |
| `<section>` | Groups thematic content (metrics, features, user directory) | Accompanied by heading via `aria-labelledby` |
| `<article>` | Encapsulates self-contained compositions (user profile cards, timeline entries) | Reusable and distributable independent units |
| `<aside>` | House notifications, sidebars, or quick-fill boxes | `role="alert"` and `aria-live="polite"` for flash notices |
| `<fieldset>` & `<legend>` | Group related input fields in web forms | Screen readers announce legend when entering field group |
| `<label for="...">` | Explicit association between title and input element | Clicking label shifts focus to input; assists WCAG compliance |
| `<table>`, `<thead>`, `<tbody>` | Presents tabular data (user records and audit logs) | Uses `<caption class="sr-only">`, `<th scope="col">`, `<th scope="row">` |
| `<figure>` & `<figcaption>` | Associates visual avatar presentation with textual metadata | Provides structured semantic captioning |
| `<time datetime="...">` | Encodes machine-readable UTC timestamps for human dates | `datetime="YYYY-MM-DDTHH:MM:SSZ"` |
| `<dl>`, `<dt>`, `<dd>` | Key-value description list for user attributes | Used in Profile view for clean metadata separation |

---

## ⚡ Instant Demo Credentials

The database is pre-seeded with 5 realistic user accounts across all roles and account statuses:

| Role | Username | Password | Email | Privileges |
| :--- | :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `Admin@12345` | `admin@cognify.com` | Full access: user editing, role changes, deletion, audit trail |
| **Manager** | `alex_manager` | `Manager@12345` | `alex.morgan@cognify.com` | Directory inspection, dashboard metrics, audit logs view |
| **Standard User** | `sarah_dev` | `User@12345` | `sarah.chen@example.com` | Profile editing, password changing, personal audit view |
| **Pending User** | `david_k` | `User@12345` | `david.kumar@example.com` | Account pending initial onboarding |
| **Suspended User**| `elena_rostova`| `User@12345` | `elena.r@example.com` | Login blocked with administrative alert |

> 💡 **Tip:** On the Sign In page (`/login`), click any of the **"One-Click Demo Credentials"** buttons to auto-populate the form instantly!

---

## 🚀 How to Run the Project

### Prerequisites
- Python 3.9+ (Python 3.10, 3.11, 3.12, 3.13, or 3.14)
- Pip (Python Package Manager)

### Step 1: Open Terminal in Project Directory
Navigate into the `HTML-Structure` folder:

```bash
cd "c:\Users\Hemanth\GitDemo.worktrees\HTML-Structure-and-Basic-Server-Interaction\HTML-Structure"
```

### Step 2: Install Dependencies (Optional if already installed)
The application requires `Flask` and `Flask-SQLAlchemy`:

```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
Launch the server using `run.py`:

```bash
python run.py
```

*Or optionally specify a custom port:*
```bash
python run.py 8080
```

*Alternative standard launch:*
```bash
python app.py
```

### Step 4: Open in Web Browser
Navigate to:
```
http://127.0.0.1:5000
```

---

## 🔍 Interactive Features to Explore

1. **Interactive Semantic Tag Inspector**:
   Click the yellow **"🏷️ Show Semantic Tags"** button in the header navbar. Notice how `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<aside>`, `<fieldset>`, and `<footer>` elements instantly gain distinctive colored dashed outlines and floating tag badges right on the screen!

2. **User Registration & Validation**:
   Navigate to `/register` and test both client-side constraints and server-side validation error handling.

3. **Role-Based Access Control**:
   - Sign in as `sarah_dev` &rarr; Notice standard user navigation (no admin link). Try accessing `/admin/dashboard` &rarr; Receives semantic `403 Forbidden` page!
   - Sign in as `admin` &rarr; Full access to user table, role assignment, account status suspension, and audit logs.

4. **Search, Filter & Pagination**:
   Navigate to `/admin/users` as `admin` or `alex_manager` to test live text search, role filtering, and status filtering with pagination.

5. **HTML Structure Educational Guide**:
   Visit `/html-guide` for a detailed breakdown of HTML5 specifications and SSR architecture.

---

## 🛡️ Security Best Practices Implemented
- **Password Hashing**: Passwords stored via `werkzeug.security` using scrypt / PBKDF2 with salt.
- **Session Protection**: HTTP-only session cookies with configurable secret key.
- **SQL Injection Prevention**: SQLAlchemy parameterized ORM queries.
- **XSS Mitigation**: Jinja2 automatic HTML escaping enabled by default.
- **RBAC Enforcement**: Explicit Python function decorators (`@login_required`, `@manager_required`, `@admin_required`).
