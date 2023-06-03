from django.urls import path
from .views import add_inv_entity_view, add_building, add_floor, add_room, add_element, dashboard_view,\
                   data_view, delete_element_view, all_data_view, export_data_view
from .crud_forms import RoomEditView, RoomDeleteView,  EntityDeleteView, EntityEditView, FloorEditView,\
                        FloorDeleteView, ElementEditView, ElementDeleteView, BuildingDeleteView, BuildingEditView

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('data/<int:entity_id>/', data_view, name='data'),
    path('data/', all_data_view, name='all_data'),
     path('export_data/<int:entity_id>/', export_data_view, name='export_data'),
    path('add_inv_entity/', add_inv_entity_view, name='add_inv_entity'),
    path('add_building/<int:entity_id>/', add_building, name='add_building'),
    path('add_floor/<int:entity_id>/', add_floor, name='add_floor'),
    path('add_room/<int:entity_id>/', add_room, name='add_room'),
    path('add_element/<int:entity_id>/', add_element, name='add_element'),
    path('delete_element/<int:element_id>/',delete_element_view, name='delete_element'),
    path('entity/<int:pk>/edit/', EntityEditView.as_view(), name='edit_entity'),
    path('entity/<int:pk>/delete/', EntityDeleteView.as_view(), name='delete_entity'),
    path('room/<int:pk>/edit/', RoomEditView.as_view(), name='edit_room'),
    path('room/<int:pk>/delete/',RoomDeleteView.as_view(), name='delete_room'),
    path('floor/<int:pk>/edit/', FloorEditView.as_view(), name='edit_floor'),
    path('floor/<int:pk>/delete/',FloorDeleteView.as_view(), name='delete_floor'),
    path('element/<int:pk>/edit/', ElementEditView.as_view(), name='edit_element'),
    path('element/<int:pk>/delete/',ElementDeleteView.as_view(), name='delete_element'),
    path('element/<int:pk>/edit/', BuildingEditView.as_view(), name='edit_building'),
    path('element/<int:pk>/delete/',BuildingDeleteView.as_view(), name='delete_building'),
]