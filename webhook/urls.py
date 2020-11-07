from django.urls import path

from . import views

app_name = 'webhook'

urlpatterns = [
    path('', views.Travis.as_view(), name='webhook'),
]
