"""
URL configuration for pravo_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.views import serve as static_serve
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from accounts.forms import LoginForm
from accounts.views import profile, register
from appeals.api import AppealViewSet
from parking.api import ParkingViewSet
from content.api import ArticleViewSet, NewsViewSet, FAQViewSet
from core.views import home, contacts
from appeals import views as appeal_views
from parking import views as parking_views
from content import views as content_views

router = DefaultRouter()
router.register('parking', ParkingViewSet, basename='api-parking')
router.register('articles', ArticleViewSet, basename='api-articles')
router.register('news', NewsViewSet, basename='api-news')
router.register('faq', FAQViewSet, basename='api-faq')
router.register('appeals', AppealViewSet, basename='api-appeals')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('static/<path:path>', static_serve, {'insecure': True}),
    path('', home, name='home'),
    path('appeals/', appeal_views.index, name='appeals'),
    path('appeals/create/', appeal_views.create, name='appeal-create'),
    path('appeals/my/', appeal_views.my_appeals, name='my-appeals'),
    path('appeals/<str:public_id>/', appeal_views.detail, name='appeal-detail'),
    path('staff/appeals/', appeal_views.staff_dashboard, name='staff-dashboard'),
    path('staff/appeals/<str:public_id>/update/', appeal_views.staff_update, name='staff-update'),
    path('parking/', parking_views.map_view, name='parking'),
    path('rights/', content_views.articles, name='rights'),
    path('rights/<slug:slug>/', content_views.article_detail, name='article-detail'),
    path('news/', content_views.news, name='news'),
    path('news/<slug:slug>/', content_views.news_detail, name='news-detail'),
    path('faq/', content_views.faq, name='faq'),
    path('contacts/', contacts, name='contacts'),
    path('accounts/register/', register, name='register'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='accounts/login.html', authentication_form=LoginForm), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('api/', include(router.urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
