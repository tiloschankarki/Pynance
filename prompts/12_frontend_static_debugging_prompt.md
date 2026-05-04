# Prompt 12 — Static Files Debugging

## Role
You are a senior Django debugging mentor.

## Goal
Debug CSS and JavaScript loading issues in a Django project.

## Context
During development, Pynance had issues where templates loaded but CSS did not apply correctly. Static file configuration needed to be checked and corrected.

## Prompt
Help debug why CSS is not loading in a Django project called Pynance. Review the static file setup, template links, folder structure, and development server behavior. Explain the likely issue step by step and provide the exact corrections needed.

## Requirements
- Check `STATIC_URL` configuration.
- Check whether `{% load static %}` is included in templates.
- Check CSS link paths.
- Check folder structure for `static/css/style.css`.
- Explain how to restart the server and hard refresh the browser.
- Avoid unrelated changes.

## Files Involved
- `settings.py`
- `templates/base.html`
- `static/css/style.css`

## Expected Output
A clear debugging path that resolves CSS loading issues.

## Verification
- Browser loads the CSS file successfully.
- Page styling appears after refresh.
- Static path errors are resolved.
