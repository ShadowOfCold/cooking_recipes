<template>
  <div>
    <h2>Создать рецепт</h2>
    <form @submit.prevent="createRecipe">
      <div>
        <label for="title">Название:</label>
        <input type="text" id="title" v-model="recipe.title" required>
      </div>

      <div>
        <label for="subcategory">Подкатегория:</label>
        <select id="subcategory" v-model="recipe.subcategory" required>
          <option v-for="subcategory in subcategories" :key="subcategory.id" :value="subcategory.id">
            {{ subcategory.name }}
          </option>
        </select>
      </div>

      <div>
        <label for="description">Описание:</label>
        <textarea id="description" v-model="recipe.description" required></textarea>
      </div>

      <div>
        <label for="prep_time">Время подготовки (мин):</label>
        <input type="number" id="prep_time" v-model.number="recipe.prep_time">
      </div>

      <div>
        <label for="cook_time">Время приготовления (мин):</label>
        <input type="number" id="cook_time" v-model.number="recipe.cook_time">
      </div>

      <div>
        <label for="servings">Количество порций:</label>
        <input type="number" id="servings" v-model.number="recipe.servings">
      </div>

      <div>
        <label for="difficulty">Сложность:</label>
        <select id="difficulty" v-model="recipe.difficulty" required>
          <option value="easy">Легко</option>
          <option value="medium">Средне</option>
          <option value="hard">Сложно</option>
        </select>
      </div>

      <div>
        <label for="image">Изображение:</label>
        <input type="file" id="image" @change="handleImageUpload">
      </div>

      <div>
        <label for="ingredients">Ингредиенты:</label>
        <input type="text" v-model="newIngredientName" placeholder="Название">
        <input type="number" v-model.number="newIngredientQuantity" placeholder="Количество">
        <input type="text" v-model="newIngredientUnit" placeholder="Единица измерения">
        <button @click.prevent="addIngredient">Добавить ингредиент</button>
        <ul>
          <li v-for="(ingredient, index) in ingredients" :key="index">
            {{ ingredient.name }} - {{ ingredient.quantity }} {{ ingredient.unit }}
            <button @click.prevent="removeIngredient(index)">Удалить</button>
          </li>
        </ul>
      </div>

      <div>
        <label for="steps">Шаги:</label>
        <textarea id="steps" v-model="recipe.steps" required></textarea>
      </div>

      <div>
        <label for="is_published">Опубликовано:</label>
        <input type="checkbox" id="is_published" v-model="recipe.is_published">
      </div>

      <button type="submit">Создать</button>
      <p v-if="error" style="color: red;">{{ error }}</p>
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
    const ingredients = ref([])

    //Для ингредиентов
    const newIngredientName = ref('');
    const newIngredientQuantity = ref(null);
    const newIngredientUnit = ref('');

    const addIngredient = () => {
      ingredients.value.push({
        name: newIngredientName.value,
        quantity: newIngredientQuantity.value,
        unit: newIngredientUnit.value,
      });
      newIngredientName.value = '';
      newIngredientQuantity.value = null;
      newIngredientUnit.value = '';
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
        ingredients.value.forEach((ingredient, index) => {
        formData.append('ingredients[name]', ingredient.name);
        formData.append('ingredients[quantity]', ingredient.quantity);
        formData.append('ingredients[unit]', ingredient.unit);
        });
        formData.append('steps', recipe.value.steps);
        formData.append('is_published', recipe.value.is_published);


        const response = await axios.post('/api/recipes/create/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });

        console.log('Recipe created:', response.data);
        router.push('/recipes');
      } catch (err) {
        error.value = err.response.data;
        console.error('Failed to create recipe', err.response.data);
      }
    };

    onMounted(async () => {
      try {
        const response = await axios.get('/api/subcategories/');
        subcategories.value = response.data;
      } catch (err) {
        error.value = 'Failed to load subcategories';
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
      ingredients
    };
  }
};
</script>
