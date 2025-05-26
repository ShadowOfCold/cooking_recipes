<template>
  <div class="recipes-page">
    <h2 class="section-title">Рецепты</h2>
    <div class="filters-container">
      <div class="filter-group">
        <input
          type="text"
          id="titleFilter"
          v-model="filters.title"
          @input="updateFilters"
          placeholder="Введите название рецепта"
          class="name-input"
        />
      </div>
    </div>

    <div class="recipes-grid">
      <div class="recipe-column">
        <h3 class="category-title">Завтрак</h3>
        <div
          v-for="recipe in breakfastRecipes"
          :key="recipe.id"
          class="recipe-card"
        >
          <router-link :to="`/recipes/${recipe.id}`" class="recipe-title">
            {{ recipe.title }}
          </router-link>
          <div class="image-wrapper">
            <img
              v-if="recipe.image"
              :src="recipe.image"
              alt="Изображение рецепта"
              class="recipe-image"
            />
            <div v-else class="placeholder-image">Нет изображения</div>
          </div>
          <p class="recipe-description">{{ recipe.description }}</p>
          <p class="recipe-info">
            <strong>Подкатегория:</strong> {{ getSubcategoryName(recipe.subcategory) }}
          </p>
          <p class="recipe-info">
            <strong>Рейтинг:</strong> {{ recipe.rating_average }} ({{ recipe.rating_count }} оценок)
          </p>
          <p class="recipe-info">
            <strong>Автор:</strong> {{ recipe.author_name }}
          </p>
        </div>
      </div>

      <div class="recipe-column">
        <h3 class="category-title">Обед</h3>
        <div
          v-for="recipe in lunchRecipes"
          :key="recipe.id"
          class="recipe-card"
        >
          <router-link :to="`/recipes/${recipe.id}`" class="recipe-title">
            {{ recipe.title }}
          </router-link>
          <div class="image-wrapper">
            <img
              v-if="recipe.image"
              :src="recipe.image"
              alt="Изображение рецепта"
              class="recipe-image"
            />
            <div v-else class="placeholder-image">Нет изображения</div>
          </div>
          <p class="recipe-description">{{ recipe.description }}</p>
          <p class="recipe-info">
            <strong>Подкатегория:</strong> {{ getSubcategoryName(recipe.subcategory) }}
          </p>
          <p class="recipe-info">
            <strong>Рейтинг:</strong> {{ recipe.rating_average }} ({{ recipe.rating_count }} оценок)
          </p>
          <p class="recipe-info">
            <strong>Автор:</strong> {{ recipe.author_name }}
          </p>
        </div>
      </div>

      <div class="recipe-column">
        <h3 class="category-title">Ужин</h3>
        <div
          v-for="recipe in dinnerRecipes"
          :key="recipe.id"
          class="recipe-card"
        >
          <router-link :to="`/recipes/${recipe.id}`" class="recipe-title">
            {{ recipe.title }}
          </router-link>
          <div class="image-wrapper">
            <img
              v-if="recipe.image"
              :src="recipe.image"
              alt="Изображение рецепта"
              class="recipe-image"
            />
            <div v-else class="placeholder-image">Нет изображения</div>
          </div>
          <p class="recipe-description">{{ recipe.description }}</p>
          <p class="recipe-info">
            <strong>Подкатегория:</strong> {{ getSubcategoryName(recipe.subcategory) }}
          </p>
          <p class="recipe-info">
            <strong>Рейтинг:</strong> {{ recipe.rating_average }} ({{ recipe.rating_count }} оценок)
          </p>
          <p class="recipe-info">
            <strong>Автор:</strong> {{ recipe.author_name }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';

export default {
  setup() {
    const recipes = ref([]);
    const loading = ref(false);
    const error = ref(null);
    const subcategories = ref([]);
    const filters = ref({
      title: '',
      subcategory: '',
    });

    const fetchRecipes = async () => {
      loading.value = true;
      error.value = null;
      try {
        const params = new URLSearchParams();
        for (const key in filters.value) {
          if (filters.value[key]) {
            params.append(key, filters.value[key]);
          }
        }
        const response = await axios.get(`/api/recipes/?${params.toString()}`);
        recipes.value = response.data;
      } catch (err) {
        error.value = 'Не удалось загрузить рецепты.';
        console.error('Failed to load recipes', err);
      } finally {
        loading.value = false;
      }
    };

    const fetchSubcategories = async () => {
      try {
        const response = await axios.get('/api/subcategories/');
        subcategories.value = response.data;
      } catch (err) {
        error.value = 'Не удалось загрузить подкатегории.';
        console.error('Failed to load subcategories', err);
      }
    };

    const updateFilters = () => {
      fetchRecipes();
    };

    const getSubcategoryName = (subcategoryId) => {
      const sub = subcategories.value.find(s => s.id === subcategoryId);
      return sub ? sub.name : 'Неизвестно';
    };

    const breakfastRecipes = computed(() => {
      return recipes.value.filter(recipe => {
        const subcategory = subcategories.value.find(s => s.id === recipe.subcategory);
        return subcategory && subcategory.category === 2;
      });
    });

    const lunchRecipes = computed(() => {
      return recipes.value.filter(recipe => {
        const subcategory = subcategories.value.find(s => s.id === recipe.subcategory);
        return subcategory && subcategory.category === 3;
      });
    });

    const dinnerRecipes = computed(() => {
      return recipes.value.filter(recipe => {
        const subcategory = subcategories.value.find(s => s.id === recipe.subcategory);
        return subcategory && subcategory.category === 4;
      });
    });

    onMounted(() => {
      fetchRecipes();
      fetchSubcategories();
    });

    return {
      recipes,
      loading,
      error,
      filters,
      subcategories,
      updateFilters,
      breakfastRecipes,
      lunchRecipes,
      dinnerRecipes,
      getSubcategoryName,
    };
  },
};
</script>

<style scoped>
.recipes-page {
  padding: 30px;
}

.recipe-title {
  font-size: 1.2em;
  font-weight: bold;
  color: #2c3e50;
  text-decoration: none;
  margin-bottom: 10px;
  text-align: center;
}

.name-input {
  width: 200px;
}

.section-title {
  text-align: center;
  font-size: 2em;
  margin-bottom: 20px;
  color: #333;
}

.filters-container {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 30px;
}

.filter-group {
  display: flex;
  flex-direction: column;
  width: 200px;
}

.filter-group label {
  font-weight: bold;
  margin-bottom: 5px;
  color: #222;
}

.filter-group input[type="text"],
.filter-group select {
  padding: 10px;
  border-radius: 6px;
  border: 1px solid #ccc;
  font-size: 16px;
}

.recipes-grid {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
  justify-content: center;
}

.recipe-column {
  flex: 1 1 30%;
  min-width: 250px;
  background: #fff;
  padding: 15px;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}

.category-title {
  text-align: center;
  margin-bottom: 15px;
  font-size: 1.5em;
  color: #444;
}

.recipe-card {
  background: #fafafa;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 15px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.recipe-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 16px rgba(0,0,0,0.2);
}

.recipe-title {
  font-size: 1.2em;
  margin-bottom: 10px;
  color: #2c3e50;
}

.image-wrapper {
  width: 100%;
  height: 350px;
  overflow: hidden;
  border-radius: 8px;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #ddd;
}

.recipe-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
}

.placeholder-image {
  font-size: 0.9em;
  color: #555;
}

.recipe-description {
  font-size: 0.95em;
  color: #555;
  overflow: hidden;
}

.recipe-info {
  font-size: 0.85em;
  color: #777;
}

@media (max-width: 768px) {
  .filters-container {
    flex-direction: column;
    align-items: center;
  }
  .recipe-column {
    flex: 1 1 100%;
  }
}
</style>
