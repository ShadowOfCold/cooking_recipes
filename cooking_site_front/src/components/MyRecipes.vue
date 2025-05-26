<template>
  <div>
    <h2>Мои рецепты</h2>
    <router-link to="/recipes/create" class="btn">Добавить рецепт</router-link>

    <div v-if="loading" class="loader">Загрузка...</div>
    <div v-else-if="recipes.length === 0" class="no-recipes">Нет ваших рецептов.</div>
    <div v-else class="my-recipes-list">
      <div v-for="recipe in recipes" :key="recipe.id" class="recipe-card">
        <router-link :to="`/recipes/${recipe.id}`" class="recipe-title">
          {{ recipe.title }}
        </router-link>
        <div class="image-container">
          <img v-if="recipe.image" :src="recipe.image" :alt="recipe.title" class="recipe-image" />
          <div v-else class="placeholder-image">Нет изображения</div>
        </div>
        <p class="description">{{ recipe.description ? recipe.description.substring(0, 100) + '...' : '' }}</p>
        <p class="rating">Рейтинг: {{ recipe.rating_average }} ({{ recipe.rating_count }} оценок)</p>
        <p class="author">Автор: {{ recipe.author_name }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';

export default {
  setup() {
    const recipes = ref([]);
    const loading = ref(true);

    const fetchMyRecipes = async () => {
      const token = localStorage.getItem('token');
      if (!token) {
        alert('Вы не авторизованы');
        loading.value = false;
        return;
      }

      try {
        const response = await fetch('/api/recipes/my/', {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${token}`,
          },
        });
        if (response.ok) {
          recipes.value = await response.json();
        } else {
          alert('Не удалось загрузить рецепты');
        }
      } catch (e) {
        console.error('Ошибка при загрузке рецептов:', e);
      } finally {
        loading.value = false;
      }
    };

    onMounted(() => {
      fetchMyRecipes();
    });

    return {
      recipes,
      loading,
    };
  },
};
</script>

<style scoped>
.btn {
  display: inline-block;
  margin-bottom: 15px;
  padding: 8px 12px;
  background-color: #4caf50;
  color: white;
  text-decoration: none;
  border-radius: 4px;
}

.btn:hover {
  background-color: #45a049;
}

.loader {
  text-align: center;
  font-size: 1.5em;
  color: #555;
}

.no-recipes {
  text-align: center;
  font-size: 1.2em;
  color: #777;
  margin-top: 20px;
}

.my-recipes-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.recipe-card {
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  padding: 15px;
  transition: transform 0.2s, box-shadow 0.2s;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.recipe-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.2);
}

.recipe-title {
  font-size: 1.2em;
  font-weight: bold;
  color: #2c3e50;
  text-decoration: none;
  margin-bottom: 10px;
  text-align: center;
}

.recipe-title:hover {
  text-decoration: underline;
}

.image-container {
  width: 100%;
  height: 150px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 10px;
  overflow: hidden;
  border-radius: 8px;
}

.recipe-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
}

.placeholder-image {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #888;
  font-size: 0.9em;
  border-radius: 8px;
}

.description {
  font-size: 0.95em;
  color: #555;
  margin-bottom: 8px;
  height: 3em;
  overflow: hidden;
  text-align: center;
}

.rating,
.author {
  font-size: 0.85em;
  color: #777;
  margin-bottom: 4px;
  text-align: center;
}
</style>
