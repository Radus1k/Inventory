from django.urls import path
from .views import signup_view, login_view, logout_view, edit_profile_view, user_data_view, users_entity_view


urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('edit_profile/', edit_profile_view, name='edit_profile'),
    path('user/<int:user_id>/', user_data_view, name='user'),
    path('user/entity/<int:entity_id>/', users_entity_view, name='users_entity'),
]