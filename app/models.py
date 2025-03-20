from django.db import models
from django.contrib.auth.models import User  # Импортируем модель User из Django

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    ingredients = models.TextField()  # Можно хранить как JSON array
    instructions = models.TextField()
    prep_time = models.IntegerField(null=True, blank=True)  # Время подготовки в минутах
    cook_time = models.IntegerField(null=True, blank=True)  # Время приготовления в минутах
    servings = models.IntegerField(null=True, blank=True)  # Количество порций
    difficulty = models.CharField(max_length=50, null=True, blank=True)  # Легкий, Средний, Сложный
    image = models.CharField(max_length=255, blank=True)  # Путь к главному изображению
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class RecipeImage(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    image_path = models.CharField(max_length=255)
    step_number = models.IntegerField()  # Номер шага, к которому относится изображение

    def __str__(self):
        return self.image_path

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField()  # Оценка от 1 до 5
    created_at = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)  # Для ответов на комментарии

    def __str__(self):
        return self.text

class FavoriteRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user', 'recipe'),)

    def __str__(self):
        return f"{self.user.username} - {self.recipe.title}"

class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class RecipeTag(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('recipe', 'tag'),)

    def __str__(self):
        return f"{self.recipe.title} - {self.tag.name}"