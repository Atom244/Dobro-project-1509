from django.contrib import admin
from .models import Article, ArticleCategory, News, FAQ, FAQCategory, Contact

for model in [Article, ArticleCategory, News, FAQ, FAQCategory, Contact]:
    admin.site.register(model)
