<template>
  <div class="home-view">
    <aside class="sidebar">
      <ul>
        <li>Рецепты</li>
        <li>Доступный ЗОЖ</li>
        <li>Закуски</li>
        <li>Салаты</li>
        <li>Первые блюда</li>
        <li>Вторые блюда</li>
        <li>Гарниры</li>
        <li>Десерты</li>
        <li>Выпечка</li>
        <li>Напитки</li>
        <li>Заготовки и консервы</li>
        <li>Соусы и маринады</li>
      </ul>
      <ul>
        <li>Спецпроекты</li>
        <li>Полезные сервисы</li>
        <li>Главное о еде</li>
        <li>Энциклопедия</li>
        <li>Для гостей «Пятёрочки»</li>
      </ul>
    </aside>

    <main class="main-content">
      <div class="search-bar">
        <input type="text" placeholder="Поиск по рецептам и материалам">
        <button>Поиск</button>
      </div>
      <div class="featured-recipe">
        <img src="https://via.placeholder.com/350x250" alt="Блины на кефире">
        <h3>Блины на кефире по-королевски</h3>
        <p>Блины на кефире получаются особенно нежными и воздушными...</p>
        <div class="recipe-meta">
          <span>❤️ 653</span>
          <span>⭐️ 4.3 (6)</span>
          <span>💬 3</span>
        </div>
      </div>

      <div class="recipe-list">
        <h2>Последние рецепты</h2>
        <RecipeCard
            v-for="recipe in placeholderRecipes"
            :key="recipe.id"
            :recipe="recipe"
        />
      </div>
    </main>
  </div>
</template>

<script>
import { defineComponent, ref } from 'vue';
import RecipeCard from '@/components/RecipeCard.vue';

export default defineComponent({
  name: 'HomeView',
  components: {
    RecipeCard,
  },
  setup() {
    const placeholderRecipes = ref([
      { id: 1, title: 'Рецепт 1', image: 'https://via.placeholder.com/200x150' },
      { id: 2, title: 'Рецепт 2', image: 'https://via.placeholder.com/200x150' },
      { id: 3, title: 'Рецепт 3', image: 'https://via.placeholder.com/200x150' },
    ]);
    return { placeholderRecipes };
  },
});
</script>

<style scoped>
.home-view {
  display: flex;
}

.sidebar {
  width: 200px;
  padding: 20px;
  background-color: #f0f0f0;
}

.sidebar ul {
  list-style: none;
  padding: 0;
}

.sidebar li {
  margin-bottom: 10px;
}

.main-content {
  flex: 1;
  padding: 20px;
}

.search-bar {
  display: flex;
  margin-bottom: 20px;
}

.search-bar input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ccc;
}

.search-bar button {
  padding: 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
}

.featured-recipe {
  margin-bottom: 20px;
  border: 1px solid #ccc;
  padding: 10px;
}

.featured-recipe img {
  max-width: 100%;
}

.recipe-meta {
  margin-top: 10px;
  display: flex;
  justify-content: space-between;
}

.recipe-meta span {
  margin-right: 10px;
}

.recipe-list {
  margin-bottom: 20px;
}

.recipe-list h2 {
  margin-bottom: 10px;
}
</style>
