from django.urls import path
from .views import CategoryList, CategoryDetail, SubcategoryList, SubcategoryDetail, RecipeList, RecipeCreate, RecipeDetail, CommentList, CommentDetail, TagList, TagDetail, RecipeTagList, RecipeTagDetail, RecipeIngredientList, RecipeIngredientDetail, RecommendedRecipeList

urlpatterns = [
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='category-detail'),
    path('subcategories/', SubcategoryList.as_view(), name='subcategory-list'),
    path('subcategories/<int:pk>/', SubcategoryDetail.as_view(), name='subcategory-detail'),
    path('recipes/', RecipeList.as_view(), name='recipe-list'),
    path('recipes/create/', RecipeCreate.as_view(), name='recipe-create'),
    path('recipes/<int:pk>/', RecipeDetail.as_view(), name='recipe-detail'),
    path('comments/', CommentList.as_view(), name='comment-list'),
    path('comments/<int:pk>/', CommentDetail.as_view(), name='comment-detail'),
    path('tags/', TagList.as_view(), name='tag-list'),
    path('tags/<int:pk>/', TagDetail.as_view(), name='tag-detail'),
    path('recipe-tags/', RecipeTagList.as_view(), name='recipe-tag-list'),
    path('recipe-tags/<int:pk>/', RecipeTagDetail.as_view(), name='recipe-tag-detail'),
    path('ingredients/', RecipeIngredientList.as_view(), name='ingredient-list'),
    path('ingredients/<int:pk>/', RecipeIngredientDetail.as_view(), name='ingredient-detail'),
    path('recipes/recommended-recipes/', RecommendedRecipeList.as_view(), name='recommended-recipe-list'),
]