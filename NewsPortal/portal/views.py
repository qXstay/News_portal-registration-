from django.shortcuts import render, get_object_or_404
from .models import Post, Author
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView
from .forms import NewsForm, ArticleForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .filters import NewsFilter
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.contrib.auth.mixins import PermissionRequiredMixin


def news_list(request):
    news = Post.objects.filter(post_type='news').order_by('-created_at')
    paginator = Paginator(news, 5)  # 5 новостей на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'portal/news_list.html', {'page_obj': page_obj})

def article_list(request):
    articles = Post.objects.filter(post_type='article').order_by('-created_at')
    paginator = Paginator(articles, 5)  # 5 статей на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'portal/article_list.html', {'page_obj': page_obj})

def news_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'portal/news_detail.html', {'post': post})

def home(request):
    return render(request, 'portal/index.html')

def search_news(request):
    news = Post.objects.filter(post_type='news').order_by('-created_at')
    news_filter = NewsFilter(request.GET, queryset=news)
    return render(request, 'portal/search.html', {'filter': news_filter, 'news': news_filter.qs})

class NewsCreateView(LoginRequiredMixin, PermissionRequiredMixin,  CreateView):
    permission_required = 'portal.add_post'
    form_class = NewsForm
    template_name = 'portal/post_edit.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'news'
        author, created = Author.objects.get_or_create(user=self.request.user)
        post.author = author
        post.save()
        form.save_m2m()
        return super().form_valid(form)

class NewsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    permission_required = 'portal.change_post'
    model = Post
    form_class = NewsForm
    template_name = 'portal/post_edit.html'
    success_url = reverse_lazy('news_list')

    def test_func(self):
        return self.get_object().author.user == self.request.user

class NewsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'portal/post_delete.html'
    success_url = reverse_lazy('news_list')

    def test_func(self):
        return self.get_object().author.user == self.request.user

class ArticleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'portal.add_post'
    form_class = ArticleForm
    template_name = 'portal/post_edit.html'
    success_url = reverse_lazy('article_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'article'
        author, created = Author.objects.get_or_create(user=self.request.user)
        post.author = author
        post.save()
        form.save_m2m()
        return super().form_valid(form)

class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'portal.change_post'
    model = Post
    form_class = ArticleForm
    template_name = 'portal/post_edit.html'
    success_url = reverse_lazy('article_list')

    def test_func(self):
        return self.get_object().author.user == self.request.user

class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'portal/post_delete.html'
    success_url = reverse_lazy('article_list')

    def test_func(self):
        return self.get_object().author.user == self.request.user


def test_func(self):
    return self.request.user.groups.filter(name='authors').exists()

@login_required
def become_author(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')  # Получаем группу authors
    user.groups.add(authors_group)
    user.save()  # Сохраняем изменения
    return redirect('home')