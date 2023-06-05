from django.db import models
from django.utils.crypto import get_random_string
import qrcode
from PIL import Image
from io import BytesIO
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.conf import settings
from django.urls import reverse

UPLOAD_TO = settings.STATIC_ROOT.join('qr_codes')
User = get_user_model()

class Entity(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User)
    is_private = models.BooleanField(default=True)
    share_link = models.CharField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.share_link:
            # Generate a random unique string for the share link
            self.share_link = get_random_string(length=32)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return "task id :" + self.id + " " + self.title

class Building(models.Model):
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    # Add other fields specific to the building
    def __str__(self):
        return "Building: " + self.name + " from entity: " + self.entity.name   

class Floor(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    # Add other fields specific to the floor
    def __str__(self):
        return "Floor: " + str(self.number) + " from building: " + self.building.name   

class Room(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    qr_code = models.CharField(max_length=255, unique=True)  # QR code associated with the room
    qr_code_image = models.ImageField(upload_to='room/qr_codes/', blank=True)

    def save(self, *args, **kwargs):
        if not self.qr_code:
            # Generate a random QR code string if it doesn't exist
            self.qr_code = get_random_string(length=12)

            # Generate full URL
            path = reverse('room_detail', kwargs={'qr_code': self.qr_code})
            full_url = settings.SITE_URL + path

            # Generate and save the QR code image
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(full_url)
            qr.make(fit=True)
            qr_image = qr.make_image(fill="black", back_color="white")
            qr_image = qr_image.resize((200, 200), Image.ANTIALIAS)

            # Create a BytesIO object to save the image
            qr_image_io = BytesIO()
            qr_image.save(qr_image_io, format='PNG')
            qr_image_io.seek(0)

            # Set the QR code image field and save the element
            self.qr_code_image.save(f'{self.qr_code}.png', qr_image_io, save=False)
        super().save(*args, **kwargs)


    def __str__(self):
        return "Room: " + self.name + " from floor: " + str(self.floor.number) + " from entity: " + self.floor.building.entity.name 


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Element(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)  # new field for category
    name = models.CharField(max_length=255)
    qr_code = models.CharField(max_length=255, unique=True)  # QR code associated with the element
    qr_code_image = models.ImageField(upload_to='qr_codes/', blank=True)
    inserted_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.qr_code:
            # Generate a random QR code string if it doesn't exist
            self.qr_code = get_random_string(length=12)

            # Generate full URL
            path = reverse('element_detail', kwargs={'qr_code': self.qr_code})
            full_url = settings.SITE_URL + path

            # Generate and save the QR code image
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(full_url)
            qr.make(fit=True)
            qr_image = qr.make_image(fill="black", back_color="white")
            qr_image = qr_image.resize((200, 200), Image.ANTIALIAS)

            # Create a BytesIO object to save the image
            qr_image_io = BytesIO()
            qr_image.save(qr_image_io, format='PNG')
            qr_image_io.seek(0)

            # Set the QR code image field and save the element
            self.qr_code_image.save(f'{self.qr_code}.png', qr_image_io, save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Element: {self.name} from room: {self.room.name} from entity: {self.room.floor.building.entity.name} in category: {self.category.name if self.category else 'N/A'}"