from django.core.management.base import BaseCommand
from feed_service.tasks import generate_facility_feed


class Command(BaseCommand):
    help = "Generate facility feed files and metadata file via Celery."

    def handle(self, *args, **options):
        self.stdout.write("Starting feed generation...")
        task = generate_facility_feed.delay()
        self.stdout.write(f"Task queued with ID: {task.id}")
        self.stdout.write(self.style.SUCCESS("Run 'celery -A facility_feed_service.celery worker' to process the task."))