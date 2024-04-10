from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.utils.text import slugify
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

from .forms import CommentForm
from .models import Post, Comment, Category


class BlogListView(ListView):
    model = Post
    paginate_by = 3

    template_name = "post/post_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["q"] = self.request.GET.get("q") or ""
        context["category"] = self.request.GET.get("category") or "-1"
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related("tags")
        category = self.request.GET.get("category")
        tag = self.request.GET.get("tag")
        q = self.request.GET.get("q")
        if category is not None and category != '-1':
            queryset = queryset.filter(category__slug=category)
        if tag is not None:
            queryset = queryset.filter(tags__slug=tag)
        if q is not None:
            queryset = queryset.filter(name__icontains=q) | queryset.filter(description__icontains=q)
        return queryset


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
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)
        # if self.request.user.is_anonymous:
        #     return HttpResponseForbidden()
        # form.instance.author = self.request.user
        # form.save()
        # return redirect("post_detail", form.cleaned_data["post"].slug)


def tr_handler404(request, exception):
    """
    Обработка ошибки 404
    """
    return render(request=request, template_name='blogs/errors/error_page.html', status=404, context={
        'title': 'Страница не найдена: 404',
        'error_message': 'К сожалению такая страница была не найдена, или перемещена',
    })


def tr_handler500(request):
    """
    Обработка ошибки 500
    """
    return render(request=request, template_name='blogs/errors/error_page.html', status=500, context={
        'title': 'Ошибка сервера: 500',
        'error_message': 'Внутренняя ошибка сайта, вернитесь на главную страницу, отчет об ошибке мы направим администрации сайта',
    })
