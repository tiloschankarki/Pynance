# Prompt 08 — Frontend Base Layout

## Role
You are a senior frontend developer working with Django templates.

## Goal
Create a clean base layout for Pynance that all pages can extend.

## Context
The application uses Django templates rather than React. The UI should feel consistent across authentication, dashboard, transactions, and settings pages.

## Prompt
Create a reusable Django base template for Pynance. The layout should include a consistent page structure, navigation area, static CSS and JavaScript links, and template blocks for page-specific content. Keep it clean, simple, and easy to extend.

## Requirements
- Include static file loading.
- Add navigation links for main app pages.
- Provide content blocks for child templates.
- Keep markup semantic and readable.
- Avoid Bootstrap if the project is using custom CSS.

## Files Involved
- `templates/base.html`
- `static/css/style.css`
- `static/js/main.js`

## Expected Output
A consistent base template that supports all major pages in the application.

## Verification
- Child templates extend the base layout correctly.
- Static CSS and JavaScript load properly.
- Navigation appears consistently across pages.
