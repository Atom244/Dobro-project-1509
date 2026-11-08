from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from .models import Article, News, FAQ, ArticleCategory


def articles(request):
    qs = Article.objects.filter(is_published=True).select_related('category')
    q = request.GET.get('q', '')
    if q:
        qs = qs.filter(title__icontains=q)
    page = Paginator(qs, 6).get_page(request.GET.get('page'))
    return render(request, 'content/articles.html', {'page': page, 'categories': ArticleCategory.objects.all(), 'q': q})


def article_detail(request, slug):
    return render(request, 'content/article_detail.html', {'article': get_object_or_404(Article, slug=slug, is_published=True)})


def news(request):
    qs = News.objects.filter(is_published=True)
    q = request.GET.get('q', '')
    if q:
        qs = qs.filter(title__icontains=q)
    return render(request, 'content/news.html', {'page': Paginator(qs, 6).get_page(request.GET.get('page')), 'q': q})


def news_detail(request, slug):
    return render(request, 'content/news_detail.html', {'item': get_object_or_404(News, slug=slug, is_published=True)})


def faq(request):
    return render(request, 'content/faq.html', {'faqs': FAQ.objects.select_related('category')})
