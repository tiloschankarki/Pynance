# Prompt 04 — Transaction Model Design

## Role
You are a senior Django data model designer.

## Goal
Design the core transaction model for Pynance.

## Context
Transactions are the main data object in the system. Users need to record income and expenses with basic details such as amount, date, category, and description.

## Prompt
Design a Django model for financial transactions in Pynance. Each transaction should belong to a specific authenticated user and include the essential fields needed for personal cash flow tracking. Keep the model simple, normalized, and suitable for dashboard aggregation later.

## Requirements
- Associate each transaction with a user.
- Include amount, category, date, and description fields.
- Support categories such as income, fixed expense, and variable expense.
- Use appropriate field types and defaults.
- Include useful string representation for admin/debugging.

## Files Involved
- `transactions/models.py`

## Expected Output
A clean Django model that supports personal transaction tracking.

## Verification
- Every transaction belongs to one user.
- Categories clearly distinguish income and expenses.
- The model supports future dashboard summaries.
- Migrations can be created and applied without errors.
