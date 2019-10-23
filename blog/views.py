from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.forms import modelform_factory
from django import forms
from django.http import HttpResponseRedirect

from .models import Post


# Create your views here.
class PostDetail(DetailView):
    model = Post
    context_object_name = 'post'


class PostList(ListView):
    model = Post
    paginate_by = 10
    context_object_name = 'posts'


class PostEditMixin:
    model = Post
    fields = ['title', 'body', 'status']

    def get_form_class(self):
        """return customize post modelform class"""
        model = self.model
        widgets = {
            'status': forms.RadioSelect(choices=Post.STATUS_CHOICES)
        }
        return modelform_factory(model, fields=self.fields, widgets=widgets)


@method_decorator(login_required, name='dispatch')
class PostCreate(PostEditMixin, CreateView):

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        if not post.publish and post.status == 'published':
            post.publish = timezone.now()
        post.save()
        self.object = post
        return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
class PostUpdate(PostEditMixin, UpdateView):
    pass


@method_decorator(login_required, name='dispatch')
class PostDelete(DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post_list')
