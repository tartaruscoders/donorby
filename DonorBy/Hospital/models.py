# from django.contrib.auth.models import User
from django.db import models


class Measurement(models.Model):
    location = models.CharField(max_length=200)
    donorLocation = models.CharField(max_length=200)
    distance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
            return f"Distance from {self.location} to {self.donorLocation} is {self.distance} km"