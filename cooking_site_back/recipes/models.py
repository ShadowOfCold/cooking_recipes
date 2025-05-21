from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.core.validators import MinValueValidator

User = settings.AUTH_USER_MODEL

def create_unique_slug(model, value, field_name='slug'):
    slug = slugify(value, allow_unicode=True)
    original_slug = slug
    n = 1
    while model.objects.filter(**{field_name: slug}).exists():
        slug = f"{original_slug}-{n}"
        n += 1
    return slug

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class Subcategory(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name="Категория")
    name = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name="Slug")

    class Meta:
        unique_together = ('category', 'name')
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"

    def __str__(self):
        return f"{self.category.name} - {self.name}"

class Recipe(models.Model):

    DIFFICULTY_EASY = 'easy'
    DIFFICULTY_MEDIUM = 'medium'
    DIFFICULTY_HARD = 'hard'

    DIFFICULTY_CHOICES = [
        (DIFFICULTY_EASY, 'Легко'),
        (DIFFICULTY_MEDIUM, 'Средне'),
        (DIFFICULTY_HARD, 'Сложно'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, verbose_name="Подкатегория")
    title = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name="Slug")
    description = models.TextField(verbose_name="Описание")
    prep_time = models.IntegerField(null=True, blank=True, verbose_name="Время подготовки (мин)")
    cook_time = models.IntegerField(null=True, blank=True, verbose_name="Время приготовления (мин)")
    servings = models.IntegerField(null=True, blank=True, verbose_name="Количество порций")
    difficulty = models.CharField(
        max_length=50,
        choices=DIFFICULTY_CHOICES,
        verbose_name="Сложность"
    )
    image = models.ImageField(upload_to='recipe_images/', blank=True, verbose_name="Изображение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    rating_average = models.FloatField(default=0.0)
    rating_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = create_unique_slug(Recipe, self.title)
        super().save(*args, **kwargs)

    def update_rating(self):
      comments = self.comments.all()
      if comments.count() > 0:
        average = sum([comment.rating for comment in comments]) / comments.count()
        self.rating_average = average
        self.rating_count = comments.count()
        self.save()

    @property
    def author_name(self):
        return self.user.username

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients', verbose_name="Рецепт")
    name = models.CharField(max_length=255, verbose_name="Название ингредиента")
    quantity = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True, verbose_name="Количество")
    unit = models.CharField(max_length=50, blank=True, verbose_name="Единица измерения (e.g., cup, tsp)")

    def __str__(self):
        return f"{self.name} - {self.quantity} {self.unit}"

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

class Step(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='steps', verbose_name="Рецепт")
    step_number = models.IntegerField(null=True, blank=True, verbose_name="Номер шага")
    description = models.TextField(verbose_name="Описание шага")

    def __str__(self):
        return f"Шаг {self.step_number} - {self.description[:50]}..."

    class Meta:
        verbose_name = "Шаг рецепта"
        verbose_name_plural = "Шаги рецепта"

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments', verbose_name="Рецепт")
    text = models.TextField(verbose_name="Текст комментария")
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name="Рейтинг")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies', verbose_name="Родительский комментарий")
    is_deleted = models.BooleanField(default=False, verbose_name="Удален")

    def __str__(self):
        return f"Комментарий от {self.user.username} к {self.recipe.title}"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

class FavoriteRecipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name="Рецепт")

    class Meta:
        unique_together = ('user', 'recipe')
        verbose_name = "Избранный рецепт"
        verbose_name_plural = "Избранные рецепты"

    def __str__(self):
        return f"{self.user.username} - {self.recipe.title}"

class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

class RecipeTag(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name="Рецепт")
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name="Тег")

    class Meta:
        unique_together = ('recipe', 'tag')
        verbose_name = "Тег рецепта"
        verbose_name_plural = "Теги рецепта"

    def __str__(self):
        return f"{self.recipe.title} - {self.tag.name}"