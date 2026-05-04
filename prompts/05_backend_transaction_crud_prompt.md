# Prompt 05 — Transaction CRUD Views

## Role
You are a senior Django backend developer.

## Goal
Implement transaction create, read, update, and delete functionality.

## Context
Pynance users need to manage their own financial records. The CRUD flow must be user-scoped so that users cannot view or modify another user's transactions.

## Prompt
Implement full CRUD functionality for the Pynance transaction model. Users should be able to list, add, edit, and delete only their own transactions. Follow Django best practices and keep the views readable for a course project.

## Requirements
- List transactions for the authenticated user only.
- Allow users to create new transactions.
- Allow users to update existing transactions they own.
- Allow users to delete existing transactions they own.
- Prevent access to transactions owned by other users.
- Use forms and templates consistently.

## Files Involved
- `transactions/views.py`
- `transactions/forms.py`
- `transactions/urls.py`
- `templates/transactions/transaction_list.html`
- `templates/transactions/transaction_form.html`

## Expected Output
A working transaction management flow connected to the logged-in user.

## Verification
- Users only see their own transactions.
- Create, edit, and delete actions work correctly.
- Invalid forms show helpful validation errors.
- URL names match template links.
