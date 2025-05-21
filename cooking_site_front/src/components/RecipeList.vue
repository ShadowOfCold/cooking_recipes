<template>
  <div>
    <h2>Рецепты</h2>

    <div class="recipe-filters">

        <div class="filter-group">
        <label for="titleFilter">Поиск по названию:</label>
        <input type="text" id="titleFilter" v-model="filters.title" @input="updateFilters" placeholder="Введите название рецепта">
        </div>

        <div class="filter-group">
        <label for="subcategoryFilter">Подкатегория:</label>
        <select id="subcategoryFilter" v-model="filters.subcategory" @change="updateFilters">
            <option value="">Все</option>
            <option v-for="subcategory in subcategories" :key="subcategory.id" :value="subcategory.id">
            {{ subcategory.name }}
            </option>
        </select>
        </div>
    </div>

    <div class="recipe-columns">
      <div class="recipe-column">
        <h3>Завтрак</h3>
        <div v-for="recipe in breakfastRecipes" :key="recipe.id" class="recipe-card">
            <h4>{{ recipe.title }}</h4>
            <img v-if="recipe.image" :src="recipe.image" alt="Изображение рецепта" class="recipe-image">
            <p>{{ recipe.description }}</p>
            <p>Подкатегория: {{ getSubcategoryName(recipe.subcategory) }}</p>
            <p>Рейтинг: {{ recipe.rating_average }} ({{ recipe.rating_count }} оценок)</p>
            <p>Автор: {{ recipe.author_name }}</p>
        </div>
      </div>

      <div class="recipe-column">
        <h3>Обед</h3>
        <div v-for="recipe in lunchRecipes" :key="recipe.id" class="recipe-card">
            <h4>{{ recipe.title }}</h4>
            <img v-if="recipe.image" :src="recipe.image" alt="Изображение рецепта" class="recipe-image">
            <p>{{ recipe.description }}</p>
            <p>Подкатегория: {{ getSubcategoryName(recipe.subcategory) }}</p>
            <p>Рейтинг: {{ recipe.rating_average }} ({{ recipe.rating_count }} оценок)</p>
            <p>Автор: {{ recipe.author_name }}</p>
        </div>
      </div>

      <div class="recipe-column">
        <h3>Ужин</h3>
        <div v-for="recipe in dinnerRecipes" :key="recipe.id" class="recipe-card">
            <h4>{{ recipe.title }}</h4>
            <img v-if="recipe.image" :src="recipe.image" alt="Изображение рецепта" class="recipe-image">
            <p>{{ recipe.description }}</p>
            <p>Подкатегория: {{ getSubcategoryName(recipe.subcategory) }}</p>
            <p>Рейтинг: {{ recipe.rating_average }} ({{ recipe.rating_count }} оценок)</p>
            <p>Автор: {{ recipe.author_name }}</p>
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
      description: '',
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
        error.value = 'Failed to load recipes';
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
        error.value = 'Failed to load subcategories';
        console.error('Failed to load subcategories', err);
      }
    };

    const updateFilters = () => {
      fetchRecipes();
    };

    const getSubcategoryName = (subcategory) => {
        const sub = subcategories.value.find(s => s.id === subcategory);
        return sub ? sub.name : 'Неизвестно';
    };

    const breakfastRecipes = computed(() => {
        return recipes.value.filter(recipe => {
            const subcategory = subcategories.value.find(s => s.id === recipe.subcategory);
            return subcategory && subcategory.category === 2; // ID категории "Завтрак"
        });
    });

    const lunchRecipes = computed(() => {
        return recipes.value.filter(recipe => {
            const subcategory = subcategories.value.find(s => s.id === recipe.subcategory);
            return subcategory && subcategory.category === 3; // ID категории "Обед"
        });
    });

    const dinnerRecipes = computed(() => {
        return recipes.value.filter(recipe => {
            const subcategory = subcategories.value.find(s => s.id === recipe.subcategory);
            return subcategory && subcategory.category === 4; // ID категории "Ужин"
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
  }
};
</script>

<style scoped>
.recipe-columns {
  display: flex;
  justify-content: space-around;
}

.recipe-column {
  width: 30%;
  padding: 10px;
  border: 1px solid #ccc;
}

.recipe-card {
  margin-bottom: 10px;
  padding: 10px;
  border: 1px solid #eee;
  background-color: #f9f9f9;
}

.recipe-image {
  width: 500px;
  height: 300px;
}

.recipe-filters {
  margin-bottom: 20px;
}

.filter-group {
  margin-bottom: 15px;
}

.filter-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: black;
}

.filter-group input[type="text"], .filter-group select {
  width: 250px;
  padding: 10px;
  border-radius: 4px;
  font-size: 16px;
}
</style>
