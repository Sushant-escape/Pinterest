from django.urls import path
from .views import signup_view, login_view, logout_view, profile_view, profile_edit, profile_delete

app_name = 'accounts'

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('profile/delete/', profile_delete, name='profile_delete'),
]
