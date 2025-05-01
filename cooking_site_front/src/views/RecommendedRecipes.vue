<template>
    <section class="recommended-recipes">
      <h2>Рекомендованные рецепты</h2>
      <ul>
        <li v-for="recipe in recommendedRecipes" :key="recipe.id">
          <router-link :to="`/recipes/${recipe.id}`">{{ recipe.title }}</router-link>
        </li>
      </ul>
    </section>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue';
import recipeService from '../services/recipeService';

export default defineComponent({
name: 'RecommendedRecipes',
setup() {
    const recommendedRecipes = ref([]);

    onMounted(async () => {
    try {
        const recipes = await recipeService.getRecommendedRecipes();
        recommendedRecipes.value = recipes;
    } catch (error) {
        console.error("Ошибка при получении рекомендованных рецептов:", error);
    }
    });

    return { recommendedRecipes };
},
});
</script>
  