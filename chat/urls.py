from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.contact, name='contact'),
    path('<int:room_id>/', views.room, name='room'),
]
