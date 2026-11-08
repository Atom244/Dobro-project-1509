from django.db import models


class Parking(models.Model):
    name = models.CharField(max_length=180)
    address = models.CharField(max_length=300)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    total_spaces = models.PositiveIntegerField(default=0)
    accessible_spaces = models.PositiveIntegerField(default=0)
    accessibility = models.CharField(max_length=250, blank=True)
    paid = models.BooleanField(default=False)
    open_24h = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['latitude', 'longitude']), models.Index(fields=['paid', 'open_24h'])]

    def __str__(self):
        return self.name
