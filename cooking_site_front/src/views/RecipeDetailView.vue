<template>
  <div class="recipe-detail">
    <div v-if="loading">Загрузка...</div>
    <div v-else-if="error">{{ error }}</div>
    <div v-else>
      <h1>{{ recipe.title }}</h1>
      <img v-if="recipe.image" :src="recipe.image" :alt="recipe.title" style="max-width: 400px;">
      <p>{{ recipe.description }}</p>
      <p>Сложность: {{ recipe.difficulty }}</p>

      <h2>Ингредиенты:</h2>
      <ul>
        <li v-for="ingredient in recipe.ingredients" :key="ingredient.id">
          {{ ingredient.name }} - {{ ingredient.quantity }} {{ ingredient.unit }}
        </li>
      </ul>
      <h2>Шаги приготовления</h2>
    </div>
  </div>
</template>

<script>
import recipeService from '../services/recipeService.js';

export default {
  props: {
    id: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      recipe: null,
      loading: true,
      error: null
    };
  },
  async mounted() {
    try {
      this.recipe = await recipeService.getRecipe(this.id);
      this.loading = false;
    } catch (error) {
      this.error = error.message;
      this.loading = false;
    }
  }
};
</script>

<style scoped>
.recipe-detail {
  padding: 20px;
}
</style>