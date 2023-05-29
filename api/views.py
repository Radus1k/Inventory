from rest_framework import generics
from .models import QRCode
from .serializers import QRCodeSerializer

class QRCodeListCreateView(generics.ListCreateAPIView):
    queryset = QRCode.objects.all()
    serializer_class = QRCodeSerializer