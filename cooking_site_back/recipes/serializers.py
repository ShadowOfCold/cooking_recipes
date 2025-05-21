from rest_framework import serializers
from .models import Category, Subcategory, Recipe, Ingredient, Step, Comment, Tag, RecipeTag

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = '__all__'

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'

class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class RecipeTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeTag
        fields = '__all__'

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'subcategory', 'prep_time', 'cook_time', 'servings', 'difficulty', 'image', 'is_published', 'author_name', 'rating_average', 'rating_count']
        read_only_fields = ['user', 'rating_average', 'rating_count', 'slug', 'created_at', 'updated_at', 'author_name']

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients', [])
        recipe = Recipe.objects.create(**validated_data)

        for ingredient_data in ingredients_data:
            Ingredient.objects.create(recipe=recipe, **ingredient_data)

        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients', None)
        if ingredients_data is not None:
            instance.ingredients.all().delete()
            for ingredient_data in ingredients_data:
                Ingredient.objects.create(recipe=instance, **ingredient_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
