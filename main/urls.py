from django.urls import path
from .views import *
from .crud_forms import *

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('data/<int:entity_id>/', data_view, name='data'),
    path('entity_settings/<int:entity_id>/', entity_settings_view, name='entity_settings'),
    path('data/', all_data_view, name='all_data'),
    path('export_data/<int:entity_id>/', export_data_view, name='export_data'),
    path('add_inv_entity/', add_inv_entity_view, name='add_inv_entity'),
    path('add_building/<int:entity_id>/', add_building, name='add_building'),
    path('add_floor/<int:entity_id>/', add_floor, name='add_floor'),
    path('add_room/<int:entity_id>/', add_room, name='add_room'),
    path('add_element/<int:entity_id>/', add_element, name='add_element'),
    path('delete_element/<int:element_id>/',delete_element_view, name='delete_element'),
    path('entity/<int:pk>/delete/', EntityDeleteView.as_view(), name='delete_entity'),
    path('room/<int:pk>/edit/', RoomEditView.as_view(), name='edit_room'),
    path('room/<int:pk>/delete/',RoomDeleteView.as_view(), name='delete_room'),
    path('floor/<int:pk>/edit/', FloorEditView.as_view(), name='edit_floor'),
    path('floor/<int:pk>/delete/',FloorDeleteView.as_view(), name='delete_floor'),
    path('element/<int:element_id>/edit/', edit_element_view, name='edit_element'),
    path('element/<int:pk>/delete/',ElementDeleteView.as_view(), name='delete_element'),
    path('building/<int:pk>/edit/', BuildingEditView.as_view(), name='edit_building'),
    path('building/<int:pk>/delete/',BuildingDeleteView.as_view(), name='delete_building'),
    path('add_user_to_entity/<str:share_link>/', add_user_to_entity, name='add_user_to_entity'),
    path('categories/<int:entity_id>/', category_list_view , name='category_list'),
    path('add_task/', add_task_view , name='add_task'),
    path('edit_task/<int:task_id>/', edit_task_view , name='edit_task'),
    path('delete_task/<int:task_id>/', delete_task_view , name='delete_task'),
]