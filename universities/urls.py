from os import name
from django.urls import path

from . import views

app_name = 'universities'

urlpatterns = [
    path('', views.UniversityMapView.as_view(), name='map'),
    path('ajax/filter/', views.filter_view, name='filter'),
    path('ajax/universities/test/', views.test_uni_list_view, name='test_uni_list'),
]