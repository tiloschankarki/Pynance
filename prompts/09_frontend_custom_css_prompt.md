# Prompt 09 — Custom CSS System

## Role
You are a senior frontend UI developer.

## Goal
Replace Bootstrap-dependent styling with a custom CSS system for Pynance.

## Context
The project initially used Bootstrap but later moved toward custom CSS for a more controlled and consistent design.

## Prompt
Create a custom CSS structure for Pynance that styles the dashboard, forms, transaction pages, buttons, cards, and navigation without relying on Bootstrap. Keep the design clean, modern, readable, and appropriate for a personal finance app.

## Requirements
- Style global layout and typography.
- Style navigation and page containers.
- Style dashboard summary cards.
- Style forms and buttons.
- Style transaction lists and action links.
- Fix scaling issues such as oversized icons or inconsistent spacing.
- Keep CSS organized and readable.

## Files Involved
- `static/css/style.css`
- Django templates using shared classes

## Expected Output
A consistent custom UI system across the application.

## Verification
- Pages no longer depend on Bootstrap classes for layout.
- CSS loads correctly across all templates.
- Forms, buttons, cards, and transaction pages look consistent.
- UI elements are properly scaled.
