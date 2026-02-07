from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('explore/', views.explore, name='explore'),
    path('download-unsplash/', views.download_unsplash_image, name='download_unsplash'),
    path('save-unsplash/', views.save_unsplash_to_board, name='save_unsplash'),
]
