from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView


# Create your views here.
class AuthorLogin(LoginView):
    pass


class AuthorLogout(LogoutView):
    pass
