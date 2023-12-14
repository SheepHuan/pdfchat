from django.urls import path,re_path
from . import views

app_name = 'ocr'
urlpatterns = [

    path('', views.nougat, name='nougat'),
    re_path(r'^result/(?P<param>\w+)/$', views.result, name='result'),
]
