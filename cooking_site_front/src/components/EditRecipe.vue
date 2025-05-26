<template>
  <div class="recipe-form-container">
    <h2 class="form-title">Редактировать рецепт</h2>
    <form @submit.prevent="updateRecipe" class="recipe-form" v-if="!loading">
      <div class="form-group">
        <label for="title">Название:</label>
        <input type="text" id="title" v-model="recipe.title" required placeholder="Введите название рецепта" />
      </div>

      <div class="form-group">
        <label for="subcategory">Подкатегория:</label>
        <select id="subcategory" v-model="recipe.subcategory" required>
          <option disabled value="">Выберите подкатегорию</option>
          <option v-for="subcategory in subcategories" :key="subcategory.id" :value="subcategory.id">
            {{ subcategory.name }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="description">Описание:</label>
        <textarea id="description" v-model="recipe.description" required placeholder="Опишите рецепт"></textarea>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="prep_time">Время подготовки (мин):</label>
          <input type="number" id="prep_time" v-model.number="recipe.prep_time" min="0" placeholder="Минуты" />
        </div>
        <div class="form-group">
          <label for="cook_time">Время приготовления (мин):</label>
          <input type="number" id="cook_time" v-model.number="recipe.cook_time" min="0" placeholder="Минуты" />
        </div>
      </div>

      <div class="form-group">
        <label for="servings">Количество порций:</label>
        <input type="number" id="servings" v-model.number="recipe.servings" min="1" placeholder="Например, 4" />
      </div>

      <div class="form-group">
        <label for="difficulty">Сложность:</label>
        <select id="difficulty" v-model="recipe.difficulty" required>
          <option value="easy">Легко</option>
          <option value="medium">Средне</option>
          <option value="hard">Сложно</option>
        </select>
      </div>

      <div class="form-group">
        <label for="image">Изображение:</label>
        <input type="file" id="image" @change="handleImageUpload" accept="image/*" />
      </div>

      <div class="ingredients-section">
        <h3>Ингредиенты</h3>
        <div class="ingredient-inputs">
          <input type="text" v-model="newIngredientName" placeholder="Название" class="ingredient-input" />
          <input type="number" v-model.number="newIngredientQuantity" placeholder="Количество" class="ingredient-input" min="0" />
          <input type="text" v-model="newIngredientUnit" placeholder="Единица измерения" class="ingredient-input" />
          <button @click.prevent="addIngredient" class="add-button">Добавить</button>
        </div>
        <ul class="ingredients-list">
          <li v-for="(ingredient, index) in recipe.ingredients" :key="index" class="ingredient-item">
            {{ ingredient.name }} - {{ ingredient.quantity }} {{ ingredient.unit }}
            <button @click.prevent="removeIngredient(index)" class="remove-button">Удалить</button>
          </li>
        </ul>
      </div>

      <div class="form-group">
        <label for="steps">Шаги:</label>
        <textarea id="steps" v-model="recipe.steps_text" required placeholder="Опишите пошагово рецепт"></textarea>
      </div>

      <div class="form-group checkbox-group">
        <label for="is_published">
          <input type="checkbox" id="is_published" v-model="recipe.is_published" />
          Опубликовать
        </label>
      </div>

      <div class="form-actions">
        <button type="submit" class="submit-button" :disabled="saving">Сохранить</button>
      </div>

      <p v-if="error" class="error-message">{{ error }}</p>
    </form>

    <div v-else class="loader">Загрузка...</div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import axios from 'axios';

export default {
  setup() {
    const route = useRoute();
    const router = useRouter();
    const recipeId = route.params.id;

    const recipe = ref({
      title: '',
      subcategory: null,
      description: '',
      prep_time: null,
      cook_time: null,
      servings: null,
      difficulty: 'easy',
      image: null,
      ingredients: [],
      steps_text: '',
      is_published: true,
    });

    const subcategories = ref([]);
    const loading = ref(true);
    const saving = ref(false);
    const error = ref(null);
    const success = ref(false);

    const newIngredientName = ref('');
    const newIngredientQuantity = ref(null);
    const newIngredientUnit = ref('');

    const token = localStorage.getItem('token');

    const fetchSubcategories = async () => {
      try {
        const res = await axios.get('/api/subcategories/', {
          headers: { Authorization: `Token ${token}` },
        });
        subcategories.value = res.data;
      } catch (e) {
        console.error('Не удалось загрузить подкатегории', e);
      }
    };

    const fetchRecipe = async () => {
      loading.value = true;
      error.value = null;
      try {
        const res = await axios.get(`/api/recipes/${recipeId}/`, {
          headers: { Authorization: `Token ${token}` },
        });
        const data = res.data;
        recipe.value.title = data.title;
        recipe.value.subcategory = data.subcategory;
        recipe.value.description = data.description;
        recipe.value.prep_time = data.prep_time;
        recipe.value.cook_time = data.cook_time;
        recipe.value.servings = data.servings;
        recipe.value.difficulty = data.difficulty;
        recipe.value.ingredients = data.ingredients || [];
        recipe.value.steps_text = data.steps_text;
        recipe.value.is_published = data.is_published;
      } catch (e) {
        error.value = 'Не удалось загрузить рецепт';
        console.error(e);
      } finally {
        loading.value = false;
      }
    };

    const addIngredient = () => {
      if (newIngredientName.value && newIngredientQuantity.value !== null) {
        recipe.value.ingredients.push({
          name: newIngredientName.value,
          quantity: newIngredientQuantity.value,
          unit: newIngredientUnit.value || '',
        });
        newIngredientName.value = '';
        newIngredientQuantity.value = null;
        newIngredientUnit.value = '';
      }
    };

    const removeIngredient = (index) => {
      recipe.value.ingredients.splice(index, 1);
    };

    const handleImageUpload = (e) => {
      const file = e.target.files[0];
      if (file) {
        recipe.value.image = file;
      }
    };

    const updateRecipe = async () => {
      saving.value = true;
      error.value = null;
      success.value = false;

      try {
        const formData = new FormData();
        formData.append('title', recipe.value.title);
        formData.append('subcategory', recipe.value.subcategory);
        formData.append('description', recipe.value.description);
        if (recipe.value.prep_time !== null) formData.append('prep_time', recipe.value.prep_time);
        if (recipe.value.cook_time !== null) formData.append('cook_time', recipe.value.cook_time);
        if (recipe.value.servings !== null) formData.append('servings', recipe.value.servings);
        formData.append('difficulty', recipe.value.difficulty);
        if (recipe.value.image instanceof File) {
          formData.append('image', recipe.value.image);
        }
        recipe.value.ingredients.forEach(ingredient => {
          formData.append('ingredients[name]', ingredient.name);
          formData.append('ingredients[quantity]', ingredient.quantity);
          formData.append('ingredients[unit]', ingredient.unit);
        });
        formData.append('steps_text', recipe.value.steps_text);
        formData.append('is_published', recipe.value.is_published);

        await axios.put(`/api/recipes/${recipeId}/`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Token ${token}`,
          },
        });

        success.value = true;
        router.push(`/recipes/${recipeId}`);
      } catch (err) {
        error.value = err.response?.data || 'Ошибка при обновлении рецепта.';
        console.error('Ошибка при обновлении рецепта', err);
      } finally {
        saving.value = false;
      }
    };

    onMounted(() => {
      fetchSubcategories();
      fetchRecipe();
    });

    return {
      recipe,
      subcategories,
      loading,
      saving,
      error,
      success,
      newIngredientName,
      newIngredientQuantity,
      newIngredientUnit,
      addIngredient,
      removeIngredient,
      handleImageUpload,
      updateRecipe,
    };
  },
};
</script>

<style scoped>
.recipe-form-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background: #fafafa;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.form-title {
  text-align: center;
  font-size: 2em;
  margin-bottom: 20px;
  color: #333;
}

.recipe-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 15px;
}

.form-group label {
  font-weight: 600;
  margin-bottom: 5px;
  color: #555;
}

.form-group input[type="text"],
.form-group input[type="number"],
.form-group textarea,
.form-group select {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 1em;
  transition: border-color 0.3s;
}

.form-group input[type="text"]:focus,
.form-group input[type="number"]:focus,
.form-group textarea:focus,
.form-group select:focus {
  border-color: #66afe9;
  outline: none;
}

.form-row {
  display: flex;
  gap: 20px;
}

.ingredients-section {
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.ingredients-section h3 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #444;
}

.ingredient-inputs {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}

.ingredient-input {
  flex: 1;
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ccc;
}

.add-button {
  padding: 8px 12px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.add-button:hover {
  background-color: #45a049;
}

.ingredients-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.ingredient-item {
  background: #fff;
  padding: 8px 12px;
  margin-bottom: 8px;
  border-radius: 4px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.remove-button {
  background: #e74c3c;
  border: none;
  padding: 5px 10px;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s;
}

.remove-button:hover {
  background: #c0392b;
}

.form-actions {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.submit-button {
  background-color: #4CAF50;
  color: white;
  padding: 12px 24px;
  font-size: 1.1em;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-button:hover {
  background-color: #4CAF50;
}

.error-message {
  color: red;
  text-align: center;
  margin-top: 15px;
  font-weight: 600;
}

.success-message {
  color: green;
  text-align: center;
  margin-top: 15px;
}

.checkbox-group {
  display: flex;
  align-items: center;
  gap: 10px;
}
</style>