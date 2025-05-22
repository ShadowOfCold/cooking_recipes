<template>
  <div class="edit-recipe">
    <h2>Редактировать рецепт</h2>
    <form @submit.prevent="saveRecipe">
      <div>
        <label for="title">Название:</label>
        <input v-model="recipe.title" id="title" required />
      </div>

      <div>
        <label for="ingredients">Ингредиенты:</label>
        <textarea v-model="recipe.ingredients" id="ingredients" required></textarea>
      </div>

      <div>
        <label for="instructions">Инструкции:</label>
        <textarea v-model="recipe.instructions" id="instructions" required></textarea>
      </div>

      <!-- Можно добавить другие поля по необходимости -->

      <button type="submit">Сохранить</button>
    </form>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';

export default {
  setup() {
    const route = useRoute();
    const router = useRouter();
    const recipeId = route.params.id;

    const recipe = ref({
      title: '',
      ingredients: '',
      instructions: '',
    });

    // Получение данных рецепта
    const fetchRecipe = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch(`/api/recipes/${recipeId}/`, {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${token}`,
          },
        });
        if (response.ok) {
          const data = await response.json();
          recipe.value = {
            title: data.title,
            ingredients: data.ingredients,
            instructions: data.instructions,
          };
        } else {
          alert('Не удалось загрузить рецепт');
        }
      } catch (e) {
        console.error(e);
      }
    };

    // Сохранение изменений
    const saveRecipe = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch(`/api/recipes/${recipeId}/`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${token}`,
          },
          body: JSON.stringify(recipe.value),
        });
        if (response.ok) {
          alert('Рецепт успешно обновлен');
          router.push(`/recipes/${recipeId}`); // переходим на страницу рецепта
        } else {
          alert('Ошибка при сохранении рецепта');
        }
      } catch (e) {
        console.error(e);
      }
    };

    onMounted(() => {
      fetchRecipe();
    });

    return {
      recipe,
      saveRecipe,
    };
  },
};
</script>

<style scoped>
/* Можно добавить стили для формы */
</style>
