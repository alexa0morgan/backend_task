from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from blogs.models import Post, Category, Comment
from .filters import PostFilter
from .serializers import PostSerializer, CategorySerializer, CommentSerializer
from rest_framework import permissions, viewsets


# https://www.django-rest-framework.org/api-guide/viewsets/
# https://www.django-rest-framework.org/api-guide/authentication/
# https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('category').prefetch_related('tags').all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter

    def get_serializer_context(self):
        return {"request": self.request}


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Comment.objects.all()
        post = self.request.query_params.get("filter[post]")
        if post is None:
            return queryset.none()
        return queryset.filter(post__slug=post)

# class PostList(generics.ListCreateAPIView):
#     queryset = Article.objects.all()
#     serializer_class = PostSerializer


# class PostDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Article.objects.all()
#     serializer_class = PostSerializer
