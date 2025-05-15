<template>
  <div class="home">
    <h1>Добро пожаловать на наш кулинарный сайт!</h1>
    <p>Здесь вы найдете лучшие рецепты со всего мира.</p>

    <h2>Рекомендованные рецепты</h2>
    <div v-if="loading">Загрузка...</div>
    <div v-else-if="error">{{ error }}</div>
    <div v-else class="recommended-recipes">
      <div v-for="recipe in recommendedRecipes" :key="recipe.id" class="recipe-card">
        <h3>
          <router-link :to="'/recipes/' + recipe.id">{{ recipe.title }}</router-link>
        </h3>
        <img v-if="recipe.image" :src="recipe.image" :alt="recipe.title" style="max-width: 150px;">
        <p>{{ recipe.description.substring(0, 100) }}...</p>
      </div>
    </div>
  </div>
</template>

<script>
import recipeService from '../services/recipeService.js';

export default {
  data() {
    return {
      recommendedRecipes: [],
      loading: true,
      error: null
    };
  },
  async mounted() {
    try {
      this.recommendedRecipes = await recipeService.getRecommendedRecipes();
      console.log(this.recommendedRecipes)
      this.loading = false;
    } catch (error) {
      this.error = error.message;
      this.loading = false;
    }
  }
};
</script>

<style scoped>
.home {
  padding: 20px;
}

.recommended-recipes {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
}

.recipe-card {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
  width: 250px;
  text-align: center;
}
</style>