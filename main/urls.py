from django.urls import path
from .views import add_entity_view, add_building, add_floor, add_room, add_element, dashboard_view,\
                   data_view, delete_element_view

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('data/', data_view, name='data'),

    path('add_entity/', add_entity_view, name='add_entity'),
    path('add_building/<int:entity_id>/', add_building, name='add_building'),
    path('add_floor/<int:entity_id>/', add_floor, name='add_floor'),
    path('add_room/<int:entity_id>/', add_room, name='add_room'),
    path('add_element/<int:entity_id>/', add_element, name='add_element'),

    path('delete_element/<int:element_id>/',delete_element_view, name='delete_element'),
]