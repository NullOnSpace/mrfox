from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import UploadFile

# Create your views here.
@method_decorator(login_required, name="dispatch")
class UploadView(CreateView):
    model = UploadFile
    success_url = reverse_lazy('blog:post_list')
    fields = ['file']
    template_name = "upload/upload.html"
