from django.urls import path

from . import views


app_name = 'blog'

urlpatterns = [
    path('<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('', views.PostList.as_view(), name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_tag_list, name='post_tag_list'),
    path('create/', views.PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', views.PostUpdate.as_view(), name='post_edit'),
    path('<int:pk>/delete/', views.PostDelete.as_view(), name='post_del'),
    path('ajax/tag/set/', views.post_tag_set, name='post_tag_set'),
]
