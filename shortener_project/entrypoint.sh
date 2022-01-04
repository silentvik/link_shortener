#!/bin/sh

export SECRET_KEY=$SECRET_KEY
export DEBUG=$DEBUG
export ALLOWED_HOSTS=$ALLOWED_HOSTS
export SITE_URL=$SITE_URL


if [[ $ENTRYPOINT_FLUSH_DB = 1 ]]
then
    echo "run FLUSH DB."
    python manage.py flush --no-input
fi

if [[ $ENTRYPOINT_MAKE_MIGRATIONS = 1 ]]
then
    echo "run MAKEMIGRATIONS."
    python manage.py makemigrations;
else
    echo "NO MAKEMIGRATIONS.";
fi

# Performing migrations
echo "run MIGRATE."
python manage.py migrate

# Another options from .env.dev
if [ $DJANGO_SUPERUSER_USERNAME ] && [ $DJANGO_SUPERUSER_EMAIL ] && [ $DJANGO_SUPERUSER_PASSWORD ]
then
  printenv | grep DJANGO_SUPERUSER_USERNAME
  printenv | grep DJANGO_SUPERUSER_EMAIL
  printenv | grep DJANGO_SUPERUSER_PASSWORD
  python manage.py create_super_user --username $DJANGO_SUPERUSER_USERNAME --password $DJANGO_SUPERUSER_PASSWORD --noinput --email $DJANGO_SUPERUSER_EMAIL
else
  echo "default DJANGO_SUPERUSER wasnt set"
fi

python manage.py collectstatic
gunicorn shortener_project.wsgi:application --bind $GUNICORN_PORT

exec "$@"