from rest_framework import generics, permissions
from rest_framework import serializers
import django_filters.rest_framework
from .models import Category, Subcategory, Recipe, Ingredient, Comment, Tag, RecipeTag
from .serializers import CategorySerializer, SubcategorySerializer, RecipeSerializer, IngredientSerializer, CommentSerializer, TagSerializer, RecipeTagSerializer
from .filters import RecipeFilter

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_staff:
            return True

        return obj.user == request.user

class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SubcategoryList(generics.ListCreateAPIView):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SubcategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class RecipeList(generics.ListAPIView):
    queryset = Recipe.objects.filter(is_published=True)
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = RecipeFilter

class RecipeCreate(generics.CreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        recipe = serializer.save(user=self.request.user)

        ingredient_names = self.request.POST.getlist('ingredients[name]')
        ingredient_quantities = self.request.POST.getlist('ingredients[quantity]')
        ingredient_units = self.request.POST.getlist('ingredients[unit]')

        for i in range(len(ingredient_names)):
            name = ingredient_names[i]
            quantity = ingredient_quantities[i]
            unit = ingredient_units[i]

            Ingredient.objects.create(recipe=recipe, name=name, quantity=quantity, unit=unit)


class RecipeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class TagList(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class RecipeTagList(generics.ListCreateAPIView):
    queryset = RecipeTag.objects.all()
    serializer_class = RecipeTagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class RecipeTagDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RecipeTag.objects.all()
    serializer_class = RecipeTagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class RecipeIngredientList(generics.ListCreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class RecipeIngredientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class RecommendedRecipeList(generics.ListAPIView):
    queryset = Recipe.objects.all().order_by('-rating_average', '-rating_count')
    serializer_class = RecipeSerializer
    pagination_class = None