#!/bin/bash

python manage.py collectstatic --noinput

python manage.py migrate

#python manage.py test
python manage.py flush

echo "from django.contrib.auth.models import User; User.objects.get(username='admin', is_superuser=True).delete()" | python manage.py shell 2> /dev/null
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', '$DJANGO_SUPERUSER_PASSWORD')" | python manage.py shell 2> /dev/null
python manage.py runserver 0.0.0.0:8000