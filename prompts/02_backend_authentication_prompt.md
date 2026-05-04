# Prompt 02 — Backend Authentication System

## Role
You are a senior Django backend developer.

## Goal
Implement the foundational authentication flow for Pynance using Django best practices.

## Context
The application requires users to create accounts, log in, log out, and access private financial data. Each user's data must remain isolated from other users.

## Prompt
Build the authentication flow for a Django application called Pynance. Use Django's built-in authentication system where appropriate and support registration, login, logout, and authenticated-only access to private pages. Make sure the implementation is clean, beginner-friendly, and aligned with Django conventions.

## Requirements
- Create registration, login, and logout views.
- Use forms with validation and clear error handling.
- Redirect users appropriately after successful login or logout.
- Protect private pages using authentication checks.
- Avoid adding unrelated features.

## Files Involved
- `accounts/views.py`
- `accounts/forms.py`
- `accounts/urls.py`
- `templates/accounts/login.html`
- `templates/accounts/register.html`

## Expected Output
Working authentication routes and templates that allow users to register, log in, and log out.

## Verification
- A new user can register successfully.
- A registered user can log in and log out.
- Invalid form submissions show useful errors.
- Unauthenticated users cannot access protected pages.
