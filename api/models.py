from django.db import models

class QRCode(models.Model):
    code = models.CharField(max_length=255)
    # Add other fields as per your requirements