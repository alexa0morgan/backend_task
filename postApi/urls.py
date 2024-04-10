from django.urls import include, path
from rest_framework import routers

from .views import PostViewSet, CategoryViewSet, CommentViewSet

# from .views import PostList, PostDetail

router = routers.DefaultRouter()
router.register('posts', PostViewSet)
router.register('categories', CategoryViewSet)
router.register('comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

# urlpatterns = [
#     path("<int:pk>/", PostDetail.as_view(), name="post_detail"),
#     path("", PostList.as_view(), name="post_list"),
# ]
