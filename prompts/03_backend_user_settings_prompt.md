# Prompt 03 — User Settings and Profile Management

## Role
You are a senior Django backend developer.

## Goal
Add a user settings page that allows authenticated users to manage basic account information.

## Context
Pynance users need a simple settings area where they can update account-related information such as username and password.

## Prompt
Create a user settings view for Pynance that allows an authenticated user to update their username and change their password. Use Django forms and validation. Keep the page focused on account management only and make sure user feedback is clear after successful or failed updates.

## Requirements
- Require authentication before accessing settings.
- Allow username updates.
- Allow password changes using Django's password validation system.
- Display success and error messages clearly.
- Keep the logic separated and easy to understand.

## Files Involved
- `accounts/views.py`
- `accounts/forms.py`
- `accounts/urls.py`
- `templates/accounts/settings.html`

## Expected Output
A functional settings page where users can safely update account details.

## Verification
- Only logged-in users can access settings.
- Username changes persist correctly.
- Password changes require valid input.
- Users receive clear feedback after submitting forms.
