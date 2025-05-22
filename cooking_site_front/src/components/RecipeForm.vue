<template>
  <div class="recipe-form-container">
    <h2 class="form-title">Создать рецепт</h2>
    <form @submit.prevent="createRecipe" class="recipe-form">
      <div class="form-group">
        <label for="title">Название:</label>
        <input type="text" id="title" v-model="recipe.title" required placeholder="Введите название рецепта">
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
          <input type="number" id="prep_time" v-model.number="recipe.prep_time" min="0" placeholder="Минуты">
        </div>
        <div class="form-group">
          <label for="cook_time">Время приготовления (мин):</label>
          <input type="number" id="cook_time" v-model.number="recipe.cook_time" min="0" placeholder="Минуты">
        </div>
      </div>

      <div class="form-group">
        <label for="servings">Количество порций:</label>
        <input type="number" id="servings" v-model.number="recipe.servings" min="1" placeholder="Например, 4">
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
        <input type="file" id="image" @change="handleImageUpload" accept="image/*">
      </div>

      <div class="ingredients-section">
        <h3>Ингредиенты</h3>
        <div class="ingredient-inputs">
          <input type="text" v-model="newIngredientName" placeholder="Название" class="ingredient-input">
          <input type="number" v-model.number="newIngredientQuantity" placeholder="Количество" class="ingredient-input" min="0">
          <input type="text" v-model="newIngredientUnit" placeholder="Единица измерения" class="ingredient-input">
          <button @click.prevent="addIngredient" class="add-button">Добавить</button>
        </div>
        <ul class="ingredients-list">
          <li v-for="(ingredient, index) in ingredients" :key="index" class="ingredient-item">
            {{ ingredient.name }} - {{ ingredient.quantity }} {{ ingredient.unit }}
            <button @click.prevent="removeIngredient(index)" class="remove-button">Удалить</button>
          </li>
        </ul>
      </div>

      <div class="form-group">
        <label for="steps">Шаги:</label>
        <textarea id="steps" v-model="recipe.steps" required placeholder="Опишите пошагово рецепт"></textarea>
      </div>

      <div class="form-group checkbox-group">
        <label for="is_published">
          <input type="checkbox" id="is_published" v-model="recipe.is_published">
          Опубликовать
        </label>
      </div>

      <div class="form-actions">
        <button type="submit" class="submit-button">Создать</button>
      </div>

      <p v-if="error" class="error-message">{{ error }}</p>
    </form>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

export default {
  setup() {
    const recipe = ref({
      title: '',
      subcategory: null,
      description: '',
      prep_time: null,
      cook_time: null,
      servings: null,
      difficulty: 'easy',
      image: null,
      steps: '',
      is_published: true,
    });
    const error = ref(null);
    const router = useRouter();
    const subcategories = ref([]);
    const ingredients = ref([]);

    const newIngredientName = ref('');
    const newIngredientQuantity = ref(null);
    const newIngredientUnit = ref('');

    const addIngredient = () => {
      if (newIngredientName.value && newIngredientQuantity.value && newIngredientUnit.value) {
        ingredients.value.push({
          name: newIngredientName.value,
          quantity: newIngredientQuantity.value,
          unit: newIngredientUnit.value,
        });
        newIngredientName.value = '';
        newIngredientQuantity.value = null;
        newIngredientUnit.value = '';
      }
    };

    const removeIngredient = (index) => {
      ingredients.value.splice(index, 1);
    };

    const handleImageUpload = (event) => {
      recipe.value.image = event.target.files[0];
    };

    const createRecipe = async () => {
      try {
        const formData = new FormData();
        formData.append('title', recipe.value.title);
        formData.append('subcategory', recipe.value.subcategory);
        formData.append('description', recipe.value.description);
        if (recipe.value.prep_time !== null) {
          formData.append('prep_time', recipe.value.prep_time);
        }
        if (recipe.value.cook_time !== null) {
          formData.append('cook_time', recipe.value.cook_time);
        }
        if (recipe.value.servings !== null) {
          formData.append('servings', recipe.value.servings);
        }
        formData.append('difficulty', recipe.value.difficulty);
        if (recipe.value.image) {
          formData.append('image', recipe.value.image);
        }
        ingredients.value.forEach((ingredient) => {
          formData.append('ingredients[name]', ingredient.name);
          formData.append('ingredients[quantity]', ingredient.quantity);
          formData.append('ingredients[unit]', ingredient.unit);
        });
        formData.append('steps_text', recipe.value.steps);
        formData.append('is_published', recipe.value.is_published);

        const response = await axios.post('/api/recipes/create/', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        });

        router.push('/recipes');
      } catch (err) {
        error.value = err.response?.data || 'Ошибка при создании рецепта.';
        console.error('Failed to create recipe', err);
      }
    };

    onMounted(async () => {
      try {
        const response = await axios.get('/api/subcategories/');
        subcategories.value = response.data;
      } catch (err) {
        error.value = 'Не удалось загрузить подкатегории.';
        console.error('Failed to load subcategories', err);
      }
    });

    return {
      recipe,
      error,
      createRecipe,
      handleImageUpload,
      subcategories,
      newIngredientName,
      newIngredientQuantity,
      newIngredientUnit,
      addIngredient,
      removeIngredient,
      ingredients,
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
  background-color: #0069d9;
}

.error-message {
  color: red;
  text-align: center;
  margin-top: 15px;
  font-weight: 600;
}

.checkbox-group {
  display: flex;
  align-items: center;
  gap: 10px;
}
</style>