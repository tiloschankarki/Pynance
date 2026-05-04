# Prompt 14 — CSV Transaction Import

## Role
You are a senior Django backend developer.

## Goal
Support CSV-based transaction import for Pynance.

## Context
Pynance allows users to upload transaction data instead of entering every transaction manually. Imported records must still belong to the authenticated user.

## Prompt
Create a simple CSV import flow for Pynance transactions. Authenticated users should be able to upload a CSV file containing transaction data such as date, amount, category, and description. Validate rows carefully and save valid transactions to the logged-in user only.

## Requirements
- Require authentication.
- Accept a CSV file upload.
- Validate required columns.
- Validate amount, date, and category values.
- Save imported transactions to the logged-in user.
- Provide clear feedback for invalid rows.
- Keep the implementation simple and suitable for a course project.

## Files Involved
- `transactions/views.py`
- `transactions/forms.py`
- `transactions/urls.py`
- `templates/transactions/import.html`

## Expected Output
A basic CSV import feature for user-owned transaction records.

## Verification
- Valid CSV rows import successfully.
- Invalid rows show useful errors.
- Imported transactions belong only to the uploading user.
- The app does not crash on malformed files.
