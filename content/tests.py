from django.test import TestCase
from django.urls import reverse
from .models import Article, ArticleCategory


class ContentTests(TestCase):
    def setUp(self):
        category = ArticleCategory.objects.create(name='Права', slug='rights')
        Article.objects.create(title='Доступность', slug='accessibility', category=category, short_description='Описание', content='Текст', is_published=True)

    def test_article_list_search_and_detail(self):
        self.assertContains(self.client.get(reverse('rights')), 'Доступность')
        self.assertContains(self.client.get(reverse('rights') + '?q=Доступность'), 'Доступность')
        self.assertEqual(self.client.get(reverse('article-detail', args=['accessibility'])).status_code, 200)
