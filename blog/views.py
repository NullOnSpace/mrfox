from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.forms import modelform_factory
from django import forms
from django.http import (HttpResponseRedirect, HttpResponseForbidden,
    HttpResponseNotAllowed, JsonResponse)
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Post

from taggit.models import Tag


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


def post_tag_list(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags__in=[tag])
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 10)
    try:
        page_obj = paginator.get_page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, 'blog/post_list.html', {
        'posts': posts, 'is_paginated': True, 'page_obj': page_obj,
    })

def post_tag_set(request):
    if request.method == 'POST':
        tags = request.POST.getlist('tags')
        print('tags:', tags)
        pk = request.POST.get('post_id')
        print('post_id:', pk)
        post = get_object_or_404(Post, pk=pk)
        if post.author != request.user:
            return HttpResponseNotAllowed('users not post author')
        post.tags.set(*tags)
        tag_objects = post.tags.all()
        tag_dict = {tag.name: tag.slug for tag in tag_objects}
        res = {'code': 'success', 'tags': tag_dict}
        return JsonResponse(res)
    else:
        return HttpResponseNotAllowed('only post allowed')
