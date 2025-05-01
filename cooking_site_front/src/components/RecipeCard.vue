<template>
    <div class="recipe-card">
      <img :src="recipe.image" :alt="recipe.title">
      <h3>{{ recipe.title }}</h3>
    </div>
</template>

<script>
import { defineComponent } from 'vue';

export default defineComponent({
name: 'RecipeCard',
props: {
    recipe: {
    type: Object,
    required: true,
    },
},
});
</script>

<style scoped>
.recipe-card {
border: 1px solid #ccc;
padding: 10px;
margin-bottom: 10px;
}

.recipe-card img {
max-width: 100%;
margin-bottom: 10px;
}
</style>
  