<template>
  <div class="my-recipes">
    <h2>Мои рецепты</h2>
    <router-link to="/my-recipes/create" class="btn">Добавить рецепт</router-link>
    <ul>
      <li v-if="loading">Загрузка...</li>
      <li v-else-if="recipes.length === 0">Нет ваших рецептов.</li>
      <li v-else v-for="recipe in recipes" :key="recipe.id">
        <h3>{{ recipe.title }}</h3>
        <router-link :to="`/my-recipes/${recipe.id}/edit`">Редактировать</router-link>
      </li>
    </ul>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';

export default {
  setup() {
    const recipes = ref([]);
    const loading = ref(true);

    // Получение текущего пользователя
    const getCurrentUser = async () => {
      const token = localStorage.getItem('token');
      if (!token) {
        alert('Вы не авторизованы');
        return null;
      }
      try {
        const response = await fetch('/api/users/me/', {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${token}`,
          },
        });
        if (response.ok) {
          const userData = await response.json();
          return userData.username;
        } else {
          alert('Не удалось получить информацию о пользователе');
          return null;
        }
      } catch (e) {
        console.error('Ошибка при получении пользователя:', e);
        return null;
      }
    };

    // Получение рецептов и фильтрация по username
    const fetchMyRecipes = async () => {
      const token = localStorage.getItem('token');
      if (!token) {
        alert('Вы не авторизованы');
        loading.value = false;
        return;
      }

      const username = await getCurrentUser();
      if (!username) {
        loading.value = false;
        return;
      }

      try {
        const response = await fetch('/api/recipes/', {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${token}`,
          },
        });
        if (response.ok) {
          const allRecipes = await response.json();
          // Фильтруем по владельцу
          recipes.value = allRecipes.filter(
            recipe => recipe.owner_username === username
          );
        } else {
          alert('Не удалось загрузить рецепты');
        }
      } catch (e) {
        console.error('Ошибка при загрузке рецептов:', e);
      } finally {
        loading.value = false;
      }
    };

    onMounted(() => {
      fetchMyRecipes();
    });

    return {
      recipes,
      loading,
    };
  },
};
</script>

<style scoped>
/* Стиль для компонента */
.my-recipes {
  padding: 20px;
}
.btn {
  display: inline-block;
  margin-bottom: 15px;
  padding: 8px 12px;
  background-color: #4caf50;
  color: white;
  text-decoration: none;
  border-radius: 4px;
}
.btn:hover {
  background-color: #45a049;
}
ul {
  list-style: none;
  padding: 0;
}
li {
  margin-bottom: 15px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
h3 {
  margin: 0 0 10px;
}
</style>