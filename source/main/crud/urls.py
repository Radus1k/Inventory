from django.urls import path
from .views import *
from .forms import *

urlpatterns = [
    # CREATE URLS
    path('add_entity/', add_entity_view , name='add_entity'),
    path('add_building/<int:entity_id>/', add_building, name='add_building'),
    path('add_floor/<int:entity_id>/', add_floor, name='add_floor'),
    path('add_room/<int:entity_id>/', add_room, name='add_room'),
    path('add_element/<int:entity_id>/', add_element, name='add_element'),
    path('add_task/', add_task_view , name='add_task'),
    # EDIT URLS
    path('entity/<int:pk>/edit/', EntityEditView.as_view(), name='edit_entity'),
    path('building/<int:pk>/edit/', BuildingEditView.as_view(), name='edit_building'),
    path('floor/<int:pk>/edit/', FloorEditView.as_view(), name='edit_floor'),
    path('room/<int:pk>/edit/', RoomEditView.as_view(), name='edit_room'),
    path('element/<int:element_id>/edit/', edit_element_view, name='edit_element'),
    path('edit_task/<int:task_id>/', edit_task_view , name='edit_task'),
    #DELETE URLS
    path('entity/<int:pk>/delete/', EntityDeleteView.as_view(), name='delete_entity'),
    path('room/<int:pk>/delete/', RoomDeleteView.as_view(), name='delete_room'),
    path('floor/<int:pk>/delete/', FloorDeleteView.as_view(), name='delete_floor'),
    path('element/<int:pk>/delete/', ElementDeleteView.as_view(), name='delete_element'),
    path('building/<int:pk>/delete/', BuildingDeleteView.as_view(), name='delete_building'),
    path('delete_task/<int:task_id>/', delete_task_view , name='delete_task'),
]