<template>
  <div id="app">
    <nav>
      <router-link to="/" class="nav-link">Главная страница</router-link>
      <router-link to="/recipes" class="nav-link">Рецепты</router-link>
      <router-link to="/recipes/create" class="nav-link">Добавить рецепт</router-link>
      <router-link to="/register" class="nav-link" v-if="!authStore.isLoggedIn">Зарегистрироваться</router-link>
      <router-link to="/login" class="nav-link" v-if="!authStore.isLoggedIn">Авторизоваться</router-link>
      <router-link to="/logout" class="nav-link" v-if="authStore.isLoggedIn" @click="logout">Выйти</router-link>
    </nav>
    <router-view/>
  </div>
</template>

<script>
import { useAuthStore } from './stores/store';
import { useRouter } from 'vue-router';
import { onMounted } from 'vue';

export default {
  setup() {
    const authStore = useAuthStore();
    const router = useRouter();

    const logout = () => {
      authStore.logout();
      router.push('/login');
    };

    onMounted(() => {
      if (authStore.token) {
        authStore.isLoggedIn = true;
      }
    });

    return {
      authStore,
      logout
    };
  }
};
</script>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: black;
}

nav a {
  font-weight: bold;
  color: black;
}

nav {
  padding: 10px;
  margin-bottom: 20px;
}

.nav-link {
  display: inline-block;
  padding: 8px 16px;
  margin-right: 10px;
  background-color: #4CAF50;
  color: white;
  text-decoration: none;
  border-radius: 4px;
}

.nav-link:hover {
  background-color: #3e8e41;
}
</style>
