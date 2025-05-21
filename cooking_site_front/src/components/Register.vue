<template>
  <div>
    <h2>Регистрация</h2>
    <form @submit.prevent="register">
      <div>
        <label for="username">Имя пользователя:</label>
        <input type="text" id="username" v-model="username" required>
      </div>
      <div>
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="email" required>
      </div>
      <div>
        <label for="firstName">Имя:</label>
        <input type="text" id="firstName" v-model="firstName" required>
      </div>
      <div>
        <label for="lastName">Фамилия:</label>
        <input type="text" id="lastName" v-model="lastName" required>
      </div>
      <div>
        <label for="password">Пароль:</label>
        <input type="password" id="password" v-model="password" required>
      </div>
      <div>
        <label for="password2">Подтвердите пароль:</label>
        <input type="password" id="password2" v-model="password2" required>
      </div>
      <button type="submit">Зарегистрироваться</button>
      <p v-if="error" style="color: red;">{{ error }}</p>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue';
import authService from '../services/authService';
import { useAuthStore } from '../stores/store';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const username = ref('');
    const email = ref('');
    const firstName = ref('');
    const lastName = ref('');
    const password = ref('');
    const password2 = ref('');
    const error = ref(null);
    const authStore = useAuthStore();
    const router = useRouter();

    const register = async () => {
      try {
        const data = await authService.register(
          username.value,
          email.value,
          firstName.value,
          lastName.value,
          password.value,
          password2.value
        );
        router.push('/login');
      } catch (err) {
        error.value = err.message;
      }
    };

    return {
      username,
      email,
      firstName,
      lastName,
      password,
      password2,
      error,
      register
    };
  }
};
</script>