from django.db import models
from django.conf import settings
from django.urls import reverse

from taggit.managers import TaggableManager

from .utils.md_normalize import normalize

from io import StringIO


# Create your models here.
class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE, related_name='posts')
    publish = models.DateTimeField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              default='draft')
    title = models.CharField(max_length=250)
    body = models.TextField()
    tags = TaggableManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.pk])

    @property
    def normalized_body(self):
        return normalize(StringIO(self.body))
