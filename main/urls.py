from django.urls import path
from .views import register_entity, add_building, add_floor, add_room, add_element, home_view

urlpatterns = [
    path('', home_view, name='home'),
    path('register_entity/', register_entity, name='register_entity'),
    path('add_building/<int:entity_id>/', add_building, name='add_building'),
    path('add_floor/<int:entity_id>/<int:building_id>/', add_floor, name='add_floor'),
    path('add_room/<int:entity_id>/<int:building_id>/<int:floor_id>/', add_room, name='add_room'),
    path('add_element/<int:entity_id>/<int:building_id>/<int:floor_id>/<int:room_id>/', add_element, name='add_element'),
]