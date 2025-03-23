#!/bin/sh
if [ "$RUN_FEED_TASK" = "true" ]; then
    echo "Running generate_feed task..."
    python manage.py generate_feed
else
    echo "Starting Gunicorn server..."
    gunicorn facility_feed.wsgi:application --bind 0.0.0.0:8000
fi