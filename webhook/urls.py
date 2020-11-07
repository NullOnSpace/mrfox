from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = 'webhook'

urlpatterns = [
    path('', csrf_exempt(views.Travis.as_view()), name='webhook'),
]
