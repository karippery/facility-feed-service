import random
from faker import Faker
from django.core.management.base import BaseCommand

from feed_service.models import Facility


fake = Faker()

class Command(BaseCommand):
    help = "Generate 10,000 fake facility records"

    def handle(self, *args, **kwargs):
        facilities = []
        for _ in range(10000):
            facilities.append(Facility(
                name=fake.company()[:255],  # Ensure it doesn't exceed 255 chars
                phone=fake.phone_number()[:20],  # Ensure it doesn't exceed 20 chars
                url=fake.url(),  # URLField handles long URLs by default
                latitude=random.uniform(-90, 90),
                longitude=random.uniform(-180, 180),
                country=fake.country()[:100],  # Ensure it doesn't exceed 100 chars
                locality=fake.city()[:100],  # Ensure it doesn't exceed 100 chars
                region=fake.state()[:100],  # Ensure it doesn't exceed 100 chars
                postal_code=fake.zipcode()[:20],  # Ensure it doesn't exceed 20 chars
                street_address=fake.street_address()[:255],  # Ensure it doesn't exceed 255 chars
            ))

        Facility.objects.bulk_create(facilities, batch_size=1000)
        self.stdout.write(self.style.SUCCESS("Successfully generated 10,000 facilities"))
