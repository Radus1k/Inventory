from django.db import models

# Create your models here.
from django.db import models
from django.utils.crypto import get_random_string

class Institute(models.Model):
    name = models.CharField(max_length=255)
    # Add other fields specific to the institute

class Building(models.Model):
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    # Add other fields specific to the building

class Floor(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    # Add other fields specific to the floor

class Room(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    qr_code = models.CharField(max_length=255, unique=True)  # QR code associated with the room

    def save(self, *args, **kwargs):
        if not self.qr_code:
            # Generate a random QR code if it doesn't exist
            self.qr_code = get_random_string(length=12)
        super().save(*args, **kwargs)
    
class Element(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    qr_code = models.CharField(max_length=255, unique=True)  # QR code associated with the element

    def save(self, *args, **kwargs):
        if not self.qr_code:
            # Generate a random QR code if it doesn't exist
            self.qr_code = get_random_string(length=12)
        super().save(*args, **kwargs)