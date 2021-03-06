from django.shortcuts import render, get_object_or_404, reverse
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
from django.core.exceptions import PermissionDenied
from django.db.models import Q

from .models import Post

from taggit.models import Tag


# Create your views here.
class BlogAppMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'blog'
        return context


class PostDetail(BlogAppMixin, DetailView):
    model = Post
    context_object_name = 'post'


class PostList(BlogAppMixin, ListView):
    model = Post
    paginate_by = 10
    context_object_name = 'posts'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            q = Q(status="published") | Q(author=self.request.user)
        else:
            q = Q(status="published")
        qs = super().get_queryset().filter(q).order_by('-created')
        return qs


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


class AuthorRequiredMixin:
    def get_object(self, query_set=None):
        object = super().get_object(query_set)
        if self.request.user == object.author:
            return object
        raise PermissionDenied("You are not allowed to do this!")


@method_decorator(login_required, name='dispatch')
class PostCreate(BlogAppMixin, PostEditMixin, CreateView):
    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        if not post.publish and post.status == 'published':
            post.publish = timezone.now()
        post.save()
        self.object = post
        return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
class PostUpdate(BlogAppMixin, AuthorRequiredMixin, PostEditMixin, UpdateView):
    def form_valid(self, form):
        post = form.save(commit=False)
        if not post.publish and post.status == 'published':
            post.publish = timezone.now()
        post.save()
        self.object = post
        return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
class PostDelete(BlogAppMixin, AuthorRequiredMixin, DeleteView):
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
        pk = request.POST.get('post_id')
        post = get_object_or_404(Post, pk=pk)
        if post.author != request.user:
            return HttpResponseNotAllowed('users not post author')
        post.tags.set(*tags)
        tag_objects = post.tags.all()
        tag_dict = {tag.name: tag.slug for tag in tag_objects}
        res = {'code': 'success', 'tags': tag_dict}
        return JsonResponse(res)
    else:
        return HttpResponseNotAllowed('only post method allowed')
