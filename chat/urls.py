from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    path('<int:room_id>/', views.room, name='room')
]
