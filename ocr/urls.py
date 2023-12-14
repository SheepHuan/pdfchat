from django.urls import path
from . import views


urlpatterns = [

    path('nougat/', views.nougat, name='nougat'),  
    path('translation/', views.translation, name='translation'),
]
