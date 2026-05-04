# Prompt 13 — Routing and Template Debugging

## Role
You are a senior Django debugging mentor.

## Goal
Resolve routing and template rendering issues in Pynance.

## Context
During development, Pynance had issues such as `NoReverseMatch`, blank delete pages, and inconsistent template loading after moving files into app-specific folders.

## Prompt
Help debug Django routing and template errors in Pynance. Focus on URL names, namespace usage, template paths, view redirects, and form actions. Explain why the error happens and provide the exact code-level corrections needed without changing unrelated parts of the project.

## Requirements
- Check URL pattern names.
- Check `{% url %}` template tags.
- Check app namespaces if used.
- Check template folder paths.
- Check view names and redirect targets.
- Explain how to verify the fix in the browser.

## Files Involved
- `transactions/urls.py`
- `transactions/views.py`
- `templates/transactions/*.html`
- Project-level `urls.py`

## Expected Output
A corrected routing and template flow that loads the expected pages.

## Verification
- Transaction list page loads.
- Add, edit, and delete links resolve correctly.
- Delete confirmation page renders instead of showing a blank page.
- No `NoReverseMatch` errors remain.
