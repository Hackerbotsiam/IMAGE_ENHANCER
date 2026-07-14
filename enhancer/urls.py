from django.urls import path
from . import views

app_name = 'enhancer'

urlpatterns = [
    path('', views.upload_view, name='upload'),
    path('download/<str:filename>/', views.download_view, name='download'),
]