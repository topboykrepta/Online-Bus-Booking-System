# BusTraveller — Django migration

This workspace adds a small Django project and a `trips` app providing CRUD functionality for bus trips.

What I added
- `manage.py` and `busproject/` (Django project skeleton)
- `trips/` app with `models.py`, `views.py`, `forms.py`, `admin.py`, and `urls.py`
- Templates in `templates/trips/` for list, detail, create/edit, and delete
- `requirements.txt` with `Django>=4.2`

Quick setup (PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Notes
- The existing static files in the workspace root (`style.css`, `main.js`, `img/`) are available to Django templates because `STATICFILES_DIRS` includes the project root. Templates use `{% load static %}` and reference files like `{% static 'style.css' %}`.
- If you want to move existing static files under a `static/` folder, update `STATICFILES_DIRS` in `busproject/settings.py` or move files accordingly.

Next steps I can take for you
- Run the setup commands here (I can run them if you want).
- Add API endpoints (DRF) or a nicer frontend.
- Add tests or CI configuration.
- Add a booking flow with M-Pesa integration (STK Push) — included in this change.

MPESA integration notes
- To use real M-Pesa Daraja STK Push, set these environment variables in your environment or in a `.env` file loaded by your runtime:
	- `MPESA_CONSUMER_KEY`
	- `MPESA_CONSUMER_SECRET`
	- `MPESA_SHORTCODE`
	- `MPESA_PASSKEY`
	- `MPESA_CALLBACK_URL` (optional)

The code includes a simulated STK Push when the env vars are not set so you can test the booking flow locally without credentials.
