from django.urls import path
from .views import QRCodeListCreateView

urlpatterns = [
    path('qrcodes/', QRCodeListCreateView.as_view(), name='qrcode-list-create'),
    # Add other URLs as per your requirements
]