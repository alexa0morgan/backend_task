from django.forms import ModelForm
from blogs.models import Comment


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
