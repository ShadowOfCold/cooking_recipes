<template>
  <div>
    <h1 class="welcome-title">Добро пожаловать на наш кулинарный сайт!</h1>

    <h2>Рекомендованные рецепты</h2>
    <div v-if="loading" class="loader">Загрузка...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="recommended-recipes">
      <div v-for="recipe in displayedRecipes" :key="recipe.id" class="recipe-card">
        <router-link :to="'/recipes/' + recipe.id" class="recipe-title">
          {{ recipe.title }}
        </router-link>
        <div class="image-container">
          <img v-if="recipe.image" :src="recipe.image" :alt="recipe.title" class="recipe-image" />
          <div v-else class="placeholder-image">Нет изображения</div>
        </div>
        <p class="description">{{ recipe.description.substring(0, 100) }}...</p>
        <p class="rating">Рейтинг: {{ recipe.rating_average }} ({{ recipe.rating_count }} оценок)</p>
        <p class="author">Автор: {{ recipe.author_name }}</p>
      </div>
    </div>
    <div class="see-all">
      <router-link to="/recipes" class="see-all-button">Посмотреть все рецепты</router-link>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      recommendedRecipes: [],
      loading: true,
      error: null,
    };
  },
  computed: {
    displayedRecipes() {
      return this.recommendedRecipes.slice(0, 10);
    },
  },
  async mounted() {
    try {
      const response = await axios.get('/api/recipes/recommended-recipes/');
      this.recommendedRecipes = response.data;
      this.loading = false;
    } catch (error) {
      this.error = 'Не удалось загрузить рецепты. Попробуйте позже.';
      this.loading = false;
    }
  },
};
</script>

<style scoped>

.welcome-title {
  text-align: center;
  font-size: 2.5em;
  margin-bottom: 20px;
  color: #333;
}

.loader {
  text-align: center;
  font-size: 1.5em;
  color: #555;
}

.error {
  color: red;
  text-align: center;
  font-size: 1.2em;
  margin-bottom: 20px;
}

.recommended-recipes {
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
}

.rating,
.author {
  font-size: 0.85em;
  color: #777;
  margin-bottom: 4px;
}

.see-all {
  text-align: center;
  margin-top: 30px;
}

.see-all-button {
  background-color: #45a049;
  color: #fff;
  padding: 12px 24px;
  font-size: 1.1em;
  border-radius: 8px;
  text-decoration: none;
  transition: background-color 0.3s;
}

.see-all-button:hover {
  background-color: #45a049;
}
</style>