from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    class Meta:
        unique_together = ('category', 'name') # Гарантирует уникальность подкатегории в пределах категории

    def __str__(self):
        return f"{self.category.name} - {self.name}"

class Recipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    prep_time = models.IntegerField(null=True, blank=True) # Время в минутах
    cook_time = models.IntegerField(null=True, blank=True) # Время в минутах
    servings = models.IntegerField(null=True, blank=True)
    difficulty = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='recipe_images/', blank=True)  # Pillow is required
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    ingredient_name = models.CharField(max_length=255)
    quantity = models.CharField(max_length=255, blank=True) # e.g., "1 cup", "1/2 tsp"

    def __str__(self):
        return f"{self.ingredient_name} - {self.quantity} ({self.recipe.title})"

class RecipeImage(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='recipe_images/steps/')
    step_number = models.IntegerField(null=True, blank=True) # Номер шага, к которому относится изображение

    def __str__(self):
        return f"Image for {self.recipe.title} - Step {self.step_number}"

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Оценка от 1 до 5
    created_at = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.recipe.title}"

class FavoriteRecipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'recipe')

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
        unique_together = ('recipe', 'tag')

    def __str__(self):
        return f"{self.recipe.title} - {self.tag.name}"