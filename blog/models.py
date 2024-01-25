import transliterate
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from utils.const import NULLABLE


class PublishedManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True).order_by('-time_update')


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, **NULLABLE, verbose_name='URL')
    content = models.TextField(**NULLABLE, verbose_name='Содержание')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    photo = models.ImageField(upload_to='photos/blog/%Y/%m/%d/', **NULLABLE, default=None, verbose_name='Фото')
    view_count = models.IntegerField(default=0, verbose_name='Количество просмотров')
    author = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.SET_NULL,
        default=None,
        **NULLABLE,
        related_name='post',
        verbose_name='Автор'
    )

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['time_create']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = transliterate.slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})
