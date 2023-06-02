# views.py
from rest_framework import generics
from main.models import Room, Element
from .serializers import RoomSerializer, ElementSerializer
from django.shortcuts import get_object_or_404, render

class RoomDetail(generics.RetrieveAPIView):
    queryset = Room.objects.all()
    lookup_field = 'qr_code'  # use the 'qr_code' field to lookup
    serializer_class = RoomSerializer

class ElementDetail(generics.RetrieveAPIView):
    queryset = Element.objects.all()
    lookup_field = 'qr_code'  # use the 'qr_code' field to lookup
    serializer_class = ElementSerializer

def room_detail(request, qr_code):
    room = get_object_or_404(Room, qr_code=qr_code)
    elements = Element.objects.filter(room=room)
    return render(request, 'room_detail.html', {'room': room, 'elements': elements})

def element_detail(request, qr_code):
    element = get_object_or_404(Element, qr_code=qr_code)
    return render(request, 'element_detail.html', {'element': element})
