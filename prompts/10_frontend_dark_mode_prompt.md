# Prompt 10 — Dark Mode Toggle

## Role
You are a senior frontend JavaScript developer.

## Goal
Add a dark mode toggle that persists user preference.

## Context
Pynance includes a settings experience and frontend customization. Dark mode should be handled client-side and remembered between page reloads.

## Prompt
Implement a simple dark mode toggle for Pynance using JavaScript and localStorage. The user's selected theme should persist after refreshing the page. Keep the implementation lightweight and compatible with Django templates.

## Requirements
- Toggle a dark-mode class on the document or body.
- Save the selected theme in localStorage.
- Load the saved preference on page load.
- Keep JavaScript simple and readable.
- Add only the CSS needed to support dark mode styling.

## Files Involved
- `static/js/main.js`
- `static/css/style.css`
- `templates/base.html`
- `templates/accounts/settings.html`

## Expected Output
A functional dark mode toggle with persistent user preference.

## Verification
- Theme changes immediately when toggled.
- Theme preference persists after refresh.
- The toggle does not break pages without the button.
