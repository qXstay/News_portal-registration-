from django import forms
from .models import Post, Category
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

class NewsForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Используем чекбоксы
        label='Категории'
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'categories']

class ArticleForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Используем тот же виджет
        label='Категории'
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'categories']



class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)  # Сохраняем пользователя
        return user

