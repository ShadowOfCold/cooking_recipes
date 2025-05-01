import django_filters
from .models import Recipe

class RecipeFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.CharFilter(field_name='subcategory__category__name', lookup_expr='iexact')
    subcategory = django_filters.CharFilter(field_name='subcategory__name', lookup_expr='iexact')
    tags = django_filters.CharFilter(field_name='recipetag__tag__name', lookup_expr='iexact')
    ingredients = django_filters.CharFilter(field_name='recipeingredient__name', lookup_expr='icontains')
    difficulty = django_filters.ChoiceFilter(choices=Recipe.DIFFICULTY_CHOICES)

    class Meta:
        model = Recipe
        fields = ['title', 'category', 'subcategory', 'tags', 'ingredients', 'difficulty']
