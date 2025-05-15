<template>
  <div class="recipe-list">
    <h1>Список рецептов</h1>
    <div v-if="loading">Загрузка...</div>
    <div v-else-if="error">{{ error }}</div>
    <div v-else>
      <div v-for="recipe in recipes" :key="recipe.id" class="recipe-card">
        <h2>
          <router-link :to="{ name: 'recipeDetail', params: { id: recipe.id } }">{{ recipe.title }}</router-link>
        </h2>
        <p>{{ recipe.description.substring(0, 100) }}...</p>
        <img v-if="recipe.image" :src="recipe.image" :alt="recipe.title" style="max-width: 200px;">
        <p>Сложность: {{ recipe.difficulty }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import recipeService from '../services/recipeService.js';

export default {
  data() {
    return {
      recipes: [],
      loading: true,
      error: null
    };
  },
  async mounted() {
    try {
      this.recipes = await recipeService.getRecipes();
      this.loading = false;
    } catch (error) {
      this.error = error.message;
      this.loading = false;
    }
  }
};
</script>

<style scoped>
.recipe-card {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
}
</style>