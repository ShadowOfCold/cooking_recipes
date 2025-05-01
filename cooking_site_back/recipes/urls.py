from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('categories/', views.CategoryList.as_view()),
    path('categories/<int:pk>/', views.CategoryDetail.as_view()),
    path('subcategories/', views.SubcategoryList.as_view()),
    path('subcategories/<int:pk>/', views.SubcategoryDetail.as_view()),
    path('recipes/', views.RecipeList.as_view()),
    path('recipes/<int:pk>/', views.RecipeDetail.as_view()),
    path('comments/', views.CommentList.as_view()),
    path('comments/<int:pk>/', views.CommentDetail.as_view()),
    path('tags/', views.TagList.as_view()),
    path('tags/<int:pk>/', views.TagDetail.as_view()),
    path('recipe_tags/', views.RecipeTagList.as_view()),
    path('recipe_tags/<int:pk>/', views.RecipeTagDetail.as_view()),
    path('recipe_ingredients/', views.RecipeIngredientList.as_view()),
    path('recipe_ingredients/<int:pk>/', views.RecipeIngredientDetail.as_view()),
    path('recipes/recommended/', views.RecommendedRecipeList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)