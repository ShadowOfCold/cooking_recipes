from rest_framework import serializers
from .models import Category, Subcategory, Recipe, Ingredient, Comment, Tag, RecipeTag, Rating

from django.contrib.auth import get_user_model

User = get_user_model()

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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'user', 'recipe', 'rating']
        read_only_fields = ['user', 'recipe']

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Оценка должна быть числом от 1 до 5.")
        return value

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, required=False)
    created_at_formatted = serializers.SerializerMethodField()
    updated_at_formatted = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ['id','title', 'description', 'ingredients', 'subcategory', 'prep_time', 'cook_time', 'servings', 'difficulty', 'image', 'steps_text', 'is_published', 'author_name', 'created_at_formatted', 'updated_at_formatted', 'rating_average', 'rating_count']
        read_only_fields = ['id','user', 'rating_average', 'rating_count', 'slug', 'created_at', 'updated_at', 'author_name']

    def get_created_at_formatted(self, obj):
        return obj.created_at.strftime('%d-%m-%Y') if obj.created_at else ''
    
    def get_updated_at_formatted(self, obj):
        return obj.updated_at.strftime('%d-%m-%Y') if obj.updated_at else ''

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients', [])
        steps_text = validated_data.pop('steps_text', '')
        recipe = Recipe.objects.create(**validated_data, steps_text=steps_text)

        for ingredient_data in ingredients_data:
            Ingredient.objects.create(recipe=recipe, **ingredient_data)

        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients', None)
        steps_text = validated_data.pop('steps_text', None)

        if ingredients_data is not None:
            instance.ingredients.all().delete()
            for ingredient_data in ingredients_data:
                Ingredient.objects.create(recipe=instance, **ingredient_data)

        if steps_text is not None:
            instance.steps_text = steps_text

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance