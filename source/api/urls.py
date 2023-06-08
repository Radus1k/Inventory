from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    # path(settings.QR_CODE_ROOM_ROUTE + '<str:qr_code>/', views.RoomDetail.as_view(), name='api_room_detail'),
    # path(settings.QR_CODE_ELEMENT_ROUTE + '<str:qr_code>/', views.ElementDetail.as_view(), name='api_element_detail'),
    path('room/<str:qr_code>/', views.room_detail, name='room_detail'),
    path('element/<str:qr_code>/', views.element_detail, name='element_detail'),
    # ... other paths ...
]