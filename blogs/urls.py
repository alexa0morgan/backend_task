from django.urls import path
from .views import (
    BlogListView,
    BlogDetailView,
    BlogCreateView,
    BlogUpdateView,
    BlogDeleteView,
    CommentCreateView,
)

urlpatterns = [
    path("create/", BlogCreateView.as_view(), name="post_create"),
    path("<int:pk>/", BlogDetailView.as_view(), name="post_detail"),
    path("comment", CommentCreateView.as_view(), name="comment_create"),
    path("<int:pk>/edit/", BlogUpdateView.as_view(), name="post_edit"),
    path("<int:pk>/delete/", BlogDeleteView.as_view(), name="post_delete"),
    path("", BlogListView.as_view(), name="post_list"),
]
