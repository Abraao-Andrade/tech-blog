from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from .models import Category, Article


class ArticleAdminForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        widget=FilteredSelectMultiple("Categories", is_stacked=False),
        queryset=Category.objects.filter(is_active=True),
    )

    class Meta:
        model = Article
        fields = "__all__"
