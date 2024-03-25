from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя")
    slug = models.SlugField()

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя")
    slug = models.SlugField()

    def __str__(self):
        return self.name


class Post(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя")
    description = models.TextField(verbose_name="Описание")
    featured_image = models.ImageField(blank=True, default="default.jpg", upload_to="images/")
    slug = models.SlugField()
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Автор")
    tags = models.ManyToManyField(Tag, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.name}"


class Comment(models.Model):
    body = models.TextField(verbose_name="Комментарий")
    author = models.ForeignKey(User, verbose_name="Автор", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author.username}: {self.body[:20]}'
