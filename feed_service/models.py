from django.db import models


class Facility(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    url = models.URLField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    country = models.CharField(max_length=100)
    locality = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    street_address = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["country"]),
            models.Index(fields=["locality"]),
            models.Index(fields=["region"]),
            models.Index(fields=["postal_code"]),
            models.Index(fields=["latitude", "longitude"]),
        ]

    def __str__(self):
        return self.name
