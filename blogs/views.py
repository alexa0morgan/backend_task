from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.utils.text import slugify
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

from .forms import CommentForm
from .models import Post, Comment


class BlogListView(ListView):
    model = Post
    paginate_by = 3
    template_name = "post/post_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related("tags")
        category = self.request.GET.get("category")
        tag = self.request.GET.get("tag")
        if category is not None:
            queryset = queryset.filter(category__slug=category)
        if tag is not None:
            queryset = queryset.filter(tags__slug=tag)
        return queryset or Post.objects.all()


class BlogDetailView(DetailView):
    model = Post
    template_name = "post/post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm
        context["comments"] = self.object.comment_set.all()
        return context


class BlogCreateView(SuccessMessageMixin, CreateView):
    model = Post
    template_name = "post/post_create.html"
    fields = ["name", "description", "featured_image", "category", "tags"]
    success_message = "%(name)s успешно создан"

    def form_valid(self, form):
        # if not self.request.user:
        #     return HttpResponseForbidden()
        form.instance.slug = slugify(form.instance.name)
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogUpdateView(SuccessMessageMixin, UpdateView):
    model = Post
    template_name = "post/post_edit.html"
    fields = ["name", "description", "featured_image", "category", "tags"]
    success_message = "%(name)s успешно обновлен"


class BlogDeleteView(DeleteView):
    model = Post
    template_name = "post/post_delete.html"
    success_url = reverse_lazy("post_list")

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author == request.user:
            return super().delete(request, *args, **kwargs)
        return HttpResponseForbidden()


class CommentCreateView(SuccessMessageMixin, CreateView):
    model = Comment
    template_name = 'post/post_detail.html'
    fields = "__all__"
    success_message = "комментарий успешно создан"

    def form_valid(self, form):
        if self.request.user.is_anonymous:
            return HttpResponseForbidden()
        form.instance.author = self.request.user
        form.save()
        return redirect("post_detail", form.cleaned_data["post"].slug)
