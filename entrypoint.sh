#!/bin/sh

if [ "$RUN_CELERY" = "true" ]; then
    echo "Starting Celery worker..."
    exec celery -A facility_feed_service worker --loglevel=info
elif [ "$RUN_FEED_TASK" = "true" ]; then
    echo "Running generate_feed task..."
    exec python manage.py generate_feed
else
    echo "Starting Gunicorn server..."
    exec gunicorn facility_feed_service.wsgi:application --bind 0.0.0.0:8000
fi