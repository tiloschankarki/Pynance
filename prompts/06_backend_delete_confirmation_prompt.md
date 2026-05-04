# Prompt 06 — Delete Confirmation Flow

## Role
You are a senior Django developer focused on safe user flows.

## Goal
Add a delete confirmation step before removing a transaction.

## Context
Deleting a financial transaction should not happen accidentally. The user should confirm the action before the record is removed.

## Prompt
Update the transaction delete flow in Pynance so that deleting a transaction first loads a confirmation page. The transaction should only be deleted after the user confirms through a POST request. Keep the flow simple and consistent with Django conventions.

## Requirements
- Use a confirmation template before deletion.
- Delete only after POST confirmation.
- Cancel action should return to the transaction list.
- Ensure the transaction belongs to the authenticated user.
- Avoid immediate deletion from a GET request.

## Files Involved
- `transactions/views.py`
- `transactions/urls.py`
- `templates/transactions/transaction_confirm_delete.html`

## Expected Output
A safer delete process that asks users to confirm before removing a transaction.

## Verification
- Visiting the delete URL shows a confirmation page.
- Confirming deletes the transaction.
- Canceling returns to the transaction list.
- Users cannot delete transactions they do not own.
