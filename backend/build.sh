#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate

# Optional: bootstrap admin user when shell access is unavailable (e.g., free Render plan).
if [ "${CREATE_SUPERUSER:-False}" = "True" ]; then
python manage.py shell -c "from django.contrib.auth import get_user_model; import os; U=get_user_model(); username=os.environ.get('DJANGO_SUPERUSER_USERNAME'); email=os.environ.get('DJANGO_SUPERUSER_EMAIL'); password=os.environ.get('DJANGO_SUPERUSER_PASSWORD'); assert username and email and password, 'Missing DJANGO_SUPERUSER_* env vars'; user, created = U.objects.get_or_create(username=username, defaults={'email': email, 'is_staff': True, 'is_superuser': True}); user.email = email; user.is_staff = True; user.is_superuser = True; user.set_password(password); user.save(); print('Superuser created' if created else 'Superuser updated')"
fi
