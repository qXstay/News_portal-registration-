from django.urls import path
from . import views
from .views import (
    NewsCreateView, NewsUpdateView, NewsDeleteView,
    ArticleCreateView, ArticleUpdateView, ArticleDeleteView
)

urlpatterns = [
    path('', views.home, name='home'),  # Главная страница
    path('news/', views.news_list, name='news_list'),  # Список новостей
    path('news/<int:post_id>/', views.news_detail, name='news_detail'),  # Детальная страница новости
    path('news/search/', views.search_news, name='news_search'),
    path('news/create/', NewsCreateView.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', NewsUpdateView.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete'),
    path('articles/', views.article_list, name='article_list'),  # Список статей
    path('articles/create/', ArticleCreateView.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
    path('become-author/', views.become_author, name='become_author')
]