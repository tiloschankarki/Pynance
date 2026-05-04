# Prompt 07 — Dashboard Aggregation Logic

## Role
You are a senior Django backend developer and data aggregation specialist.

## Goal
Build the dashboard logic that summarizes user financial activity.

## Context
The dashboard is the main page where users quickly understand their income, expenses, balance, recent transactions, and monthly summary.

## Prompt
Create a Django dashboard view for Pynance that aggregates financial data for the authenticated user. The dashboard should calculate total income, total expenses, net balance, show recent transactions, and provide a basic monthly summary using Django ORM aggregation.

## Requirements
- Scope all calculations to the logged-in user.
- Calculate total income.
- Calculate total expenses.
- Calculate net balance.
- Display recent transactions.
- Prepare a monthly summary for dashboard display.
- Keep logic clear and maintainable.

## Files Involved
- `dashboard/views.py`
- `dashboard/urls.py`
- `templates/dashboard/dashboard.html`

## Expected Output
A dashboard view that gives users quick financial insight based on their own transaction history.

## Verification
- Totals are accurate for the logged-in user.
- Other users' transactions are excluded.
- Empty transaction states do not break the page.
- Dashboard context values render correctly in the template.
