from django.db import models


class ArticleCategory(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=220)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(ArticleCategory, on_delete=models.PROTECT, related_name='articles')
    short_description = models.CharField(max_length=400)
    content = models.TextField()
    image = models.ImageField(upload_to='articles/', blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-published_at', '-id']

    def __str__(self):
        return self.title


class News(models.Model):
    title = models.CharField(max_length=220)
    slug = models.SlugField(unique=True)
    preview = models.CharField(max_length=400)
    content = models.TextField()
    image = models.ImageField(upload_to='news/', blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-published_at', '-id']

    def __str__(self):
        return self.title


class FAQCategory(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class FAQ(models.Model):
    category = models.ForeignKey(FAQCategory, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=300)
    answer = models.TextField()
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'id']
        verbose_name = 'Вопрос FAQ'
        verbose_name_plural = 'FAQ'

    def __str__(self):
        return self.question


class Contact(models.Model):
    title = models.CharField(max_length=160)
    value = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'title']

    def __str__(self):
        return self.title
