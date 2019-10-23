from django.urls import path

from . import views


urlpatterns = [
    path('sign-in/', views.AuthorLogin.as_view(), name='login'),
    path('sign-out/', views.AuthorLogout.as_view(), name='logout'),
]
