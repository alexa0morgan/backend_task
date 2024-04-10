from rest_framework import serializers

from blogs.models import Post, Category, Tag, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "name",
            "slug",
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            "name",
            "slug",
        )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        model = Comment
        fields = (
            "author",
            "body",
        )


class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tags = TagSerializer(many=True)
    comments = serializers.SerializerMethodField(read_only=True)
    author = serializers.SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        model = Post
        fields = (
            "name",
            "description",
            "author",
            "category",
            "tags",
            "slug",
            "comments",
        )

    def request_has_include_comments(self):
        request = self.context.get("request")
        return request and request.query_params.get("include") == "comments"

    def get_comments(self, instance):
        if self.request_has_include_comments():
            return CommentSerializer(instance.comment_set.all(), many=True).data
        return None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not self.request_has_include_comments():
            data.pop("comments")
        return data
