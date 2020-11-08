from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse, HttpResponseForbidden


# Create your views here.
class AuthorLogin(LoginView):
    pass


class AuthorLogout(LogoutView):
    pass


def auth(request):
    if request.user.is_authenticated:
        return HttpResponse("OK")
    return HttpResponseForbidden()
