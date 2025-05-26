<template>
  <div class="recipe-detail" v-if="recipe">
    <h1 class="title">{{ recipe.title }}</h1>
    <img
      v-if="recipe.image"
      :src="recipe.image"
      alt="Изображение рецепта"
      class="recipe-image"
    />

    <div class="info">
      <p><strong>Описание:</strong> {{ recipe.description }}</p>
      <p><strong>Время подготовки:</strong> {{ recipe.prep_time }} мин</p>
      <p><strong>Время приготовления:</strong> {{ recipe.cook_time }} мин</p>
      <p><strong>Порций:</strong> {{ recipe.servings }}</p>
      <p><strong>Сложность:</strong> {{ difficultyLabel }}</p>
    </div>

    <section class="ingredients">
      <h2>Ингредиенты</h2>
      <ul>
        <li v-for="ingredient in recipe.ingredients" :key="ingredient.id">
          {{ ingredient.name }} - {{ ingredient.quantity }} {{ ingredient.unit }}
        </li>
      </ul>
    </section>

    <section class="steps">
      <h2>Шаги</h2>
      <div class="steps-text" v-if="recipe.steps_text" v-html="recipe.steps_text"></div>
      <div v-else>Нет шагов</div>
    </section>

    <div class="info">
      <p><strong>Дата создания:</strong> {{ recipe.created_at_formatted }}</p>
      <p><strong>Дата последнего обновления:</strong> {{ recipe.updated_at_formatted }}</p>
      <p>
        <strong>Рейтинг:</strong> {{ recipe.rating_average.toFixed(1) }}
        ({{ recipe.rating_count }} отзывов)
      </p>
    </div>

    <div class="rating-section">
      <h3>Оцените рецепт</h3>
      <div class="stars">
        <span
          v-for="star in 5"
          :key="star"
          @click="setRating(star)"
          style="cursor: pointer; margin-right: 5px;"
        >
          <i :class="star <= userRating ? 'fas fa-star' : 'far fa-star'"></i>
        </span>
      </div>
    </div>

    <div class="author-actions" v-if="isAuthor">
      <button @click="goToEdit" class="btn btn-edit">Редактировать</button>
      <button @click="deleteRecipe" class="btn btn-delete">Удалить</button>
    </div>
  </div>

  <div v-else class="loading">Загрузка рецепта...</div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';

export default {
  setup() {
    const route = useRoute();
    const router = useRouter();
    const recipeId = route.params.id;
    const recipe = ref(null);
    const userRating = ref(0);
    const currentUsername = ref(null);

    const fetchCurrentUser = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch('/api/users/me/', {
          headers: {
            Authorization: `Token ${token}`,
          },
        });
        if (response.ok) {
          const data = await response.json();
          currentUsername.value = data.username;
        } else {
          console.error('Не удалось получить текущего пользователя');
        }
      } catch (e) {
        console.error('Ошибка при получении текущего пользователя', e);
      }
    };

    const fetchRecipe = async () => {
      try {
        const response = await fetch(`/api/recipes/${recipeId}/`);
        if (response.ok) {
          recipe.value = await response.json();
        } else {
          console.error('Ошибка загрузки рецепта');
        }
      } catch (error) {
        console.error('Ошибка:', error);
      }
    };

    const setRating = async (star) => {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch(`/api/recipes/${recipeId}/ratings/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Token ${token}`,
          },
          body: JSON.stringify({ rating: star }),
        });
        if (response.ok) {
          await fetchRatingData();
          userRating.value = star;
        } else {
          alert('Ошибка при отправке оценки');
        }
      } catch (e) {
        console.error(e);
      }
    };

    const fetchRatingData = async () => {
      try {
        const res = await fetch(`/api/recipes/${recipeId}/ratings/average/`);
        if (res.ok) {
          const data = await res.json();
          if (recipe.value) {
            recipe.value.rating_average = data.average;
            recipe.value.rating_count = data.count;
          }
        }
      } catch (e) {
        console.error('Ошибка при загрузке рейтинга', e);
      }
    };

    const difficultyLabel = computed(() => {
      if (!recipe.value) return '';
      switch (recipe.value.difficulty) {
        case 'easy':
          return 'Легко';
        case 'medium':
          return 'Средне';
        case 'hard':
          return 'Сложно';
        default:
          return '';
      }
    });

    const isAuthor = computed(() => {
      if (!recipe.value || !currentUsername.value) return false;
      return recipe.value.author_name === currentUsername.value;
    });

    const goToEdit = () => {
      router.push(`/my-recipes/${recipeId}/edit`);
    };

    const deleteRecipe = async () => {
      if (!confirm('Вы действительно хотите удалить этот рецепт?')) return;
      try {
        const token = localStorage.getItem('token');
        const response = await fetch(`/api/recipes/${recipeId}/`, {
          method: 'DELETE',
          headers: {
            Authorization: `Token ${token}`,
          },
        });
        if (response.ok) {
          alert('Рецепт успешно удалён');
          router.push('/my-recipes');
        } else {
          alert('Ошибка при удалении рецепта');
        }
      } catch (e) {
        console.error('Ошибка удаления:', e);
        alert('Ошибка при удалении рецепта');
      }
    };

    onMounted(async () => {
      await fetchCurrentUser();
      await fetchRecipe();
      await fetchRatingData();
    });

    return {
      recipe,
      userRating,
      setRating,
      difficultyLabel,
      isAuthor,
      goToEdit,
      deleteRecipe,
    };
  },
};
</script>

<style scoped>
.recipe-detail {
  max-width: 900px;
  margin: 20px auto;
  padding: 20px;
  font-family: 'Arial', sans-serif;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.title {
  text-align: center;
  margin-bottom: 15px;
  font-size: 2em;
  color: #2c3e50;
}

.recipe-image {
  display: block;
  max-width: 100%;
  border-radius: 12px;
  margin: 0 auto 20px;
}

.info p {
  margin: 5px 0;
  line-height: 1.4;
}

.stars i {
  color: #f39c12;
  font-size: 2em;
}

h2 {
  margin-top: 30px;
  margin-bottom: 15px;
  font-size: 1.75em;
  color: #34495e;
}

ul,
ol {
  padding-left: 20px;
}

li {
  margin-bottom: 8px;
  font-size: 1em;
  list-style-type: none;
}

.stars {
  font-size: 1.5em;
  cursor: pointer;
  color: #f39c12;
}

.loading {
  text-align: center;
  font-size: 1.5em;
  margin-top: 50px;
}

.author-actions {
  margin-top: 30px;
  display: flex;
  gap: 15px;
  justify-content: center;
}

.btn {
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  border: none;
  font-size: 1em;
  transition: background-color 0.3s ease;
}

.btn-edit {
  background-color: #45a049;
  color: white;
}

.btn-edit:hover {
  background-color: #45a049;
}

.btn-delete {
  background-color: #e74c3c;
  color: white;
}

.btn-delete:hover {
  background-color: #c0392b;
}

@media (max-width: 768px) {
  .recipe-detail {
    padding: 10px;
  }
}
</style>
