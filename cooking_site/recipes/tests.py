from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Recipe, Subcategory, Category
from django.core.exceptions import ValidationError

class RecipeModelTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.category = Category.objects.create(name="Тестовая категория")
        self.subcategory = Subcategory.objects.create(name='Тестовая подкатегория', slug='test-subcategory', category=self.category)
        self.recipe_data = {
            'user': self.user,
            'subcategory': self.subcategory,
            'title': 'Тестовый рецепт',
            'description': 'Описание тестового рецепта',
            'prep_time': 30,
            'cook_time': 45,
            'servings': 4,
            'difficulty': Recipe.DIFFICULTY_MEDIUM,
        }


    def test_recipe_creation(self):
        """Тест: Убедитесь, что Recipe создается правильно."""
        recipe = Recipe.objects.create(**self.recipe_data)
        self.assertEqual(recipe.title, 'Тестовый рецепт')
        self.assertEqual(recipe.difficulty, Recipe.DIFFICULTY_MEDIUM)
        self.assertEqual(recipe.user, self.user)
        self.assertEqual(recipe.subcategory, self.subcategory)

    def test_recipe_difficulty_choices(self):
        """Тест: Убедитесь, что поле difficulty имеет правильные варианты выбора."""
        recipe = Recipe.objects.create(**self.recipe_data)
        difficulty_choices = dict(Recipe.DIFFICULTY_CHOICES)
        self.assertIn(recipe.difficulty, difficulty_choices)
        self.assertEqual(difficulty_choices[recipe.difficulty], 'Средне')

    def test_recipe_string_representation(self):
        """Тест: Убедитесь, что метод __str__ работает правильно."""
        recipe = Recipe.objects.create(**self.recipe_data)
        self.assertEqual(str(recipe), 'Тестовый рецепт')

    def test_recipe_no_blank_difficulty(self):
        """Тест: Убедитесь, что нельзя создать Recipe без difficulty (поле обязательно)."""
        original_difficulty = self.recipe_data['difficulty']
        del self.recipe_data['difficulty']
        with self.assertRaises(ValidationError):
            recipe = Recipe(**self.recipe_data)
            recipe.full_clean()

            self.fail("Должно было возникнуть исключение ValidationError")

        self.recipe_data['difficulty'] = original_difficulty
