from django.db import models

class Facility(models.Model):
    name = models.CharField(max_length=255, db_index=True)  # Frequently searched field
    phone = models.CharField(max_length=20)
    url = models.URLField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    country = models.CharField(max_length=100, db_index=True)  # Frequently filtered field
    locality = models.CharField(max_length=100, db_index=True)
    region = models.CharField(max_length=100, db_index=True)
    postal_code = models.CharField(max_length=20, db_index=True)  # Searching by postal code
    street_address = models.CharField(max_length=255)

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["country"]),
            models.Index(fields=["locality"]),
            models.Index(fields=["region"]),
            models.Index(fields=["postal_code"]),
        ]

    def __str__(self):
        return self.name