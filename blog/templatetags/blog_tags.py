from django.utils.safestring import mark_safe
from django.template import Library

import markdown

from ..models import Post


register = Library()


@register.filter(name="markdown")
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


@register.simple_tag(name="my_posts")
def get_user_n_latest_posts(user, n=10):
    return user.posts.filter(status='published').order_by('-publish')[:n]


@register.simple_tag(name='latest_posts')
def get_n_latest_posts(n=10):
    return Post.objects.filter(status="published")[:n]
