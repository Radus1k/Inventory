from django.urls import path, include
from .views import dashboard_view, data_view,entity_settings_view, users_entity_view,\
            export_data_view, add_user_to_entity_view, category_list_view, accept_request_view, deny_request_view, map_view

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('data/<int:entity_id>/', data_view, name='data'),
    path('entity_settings/<int:entity_id>/', entity_settings_view, name='entity_settings'),
    path('export_data/<int:entity_id>/', export_data_view, name='export_data'),
    path('location/<int:entity_id>/', map_view, name='location'),

    path('user/entity/<int:entity_id>/', users_entity_view, name='users_entity'),
    path('add_user_to_entity/<str:share_link>/', add_user_to_entity_view, name='add_user_to_entity'),
    path('categories/<int:entity_id>/', category_list_view , name='category_list'),
    path('accept_request/<int:request_id>/', accept_request_view, name='accept_request'),
    path('deny_request/<int:request_id>/', deny_request_view, name='deny_request'),
    path('crud/', include('main.crud.urls')),  # Include the CRUD app's URLs
]