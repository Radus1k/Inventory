# views.py
from rest_framework import generics
from main.models import Room, Element
from .serializers import RoomSerializer, ElementSerializer
from django.shortcuts import get_object_or_404, render
from django.db.models import F

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

    element.access_count = F('access_count') + 1
    element.save(update_fields=['access_count'])

    return render(request, 'element_detail.html', {'element': element})
