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
