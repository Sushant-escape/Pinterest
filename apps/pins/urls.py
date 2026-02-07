from django.urls import path
from . import views

app_name = 'pins'

urlpatterns = [
    path('create/', views.pin_create, name='pin_create'),
    path('<int:pin_id>/', views.pin_detail, name='pin_detail'),
    path('<int:pin_id>/edit/', views.pin_edit, name='pin_edit'),
    path('<int:pin_id>/delete/', views.pin_delete, name='pin_delete'),
    path('<int:pin_id>/save/', views.pin_save, name='pin_save'),
]
