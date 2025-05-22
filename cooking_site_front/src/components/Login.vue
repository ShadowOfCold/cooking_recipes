<template>
  <div class="login-container">
    <h2 class="section-title">Вход</h2>
    <form @submit.prevent="login" class="login-form">
      <div class="form-group">
        <label for="username">Имя пользователя</label>
        <input
          type="text"
          id="username"
          v-model="username"
          required
          placeholder="Введите имя пользователя"
        />
      </div>
      
      <div class="form-group">
        <label for="password">Пароль</label>
        <input
          type="password"
          id="password"
          v-model="password"
          required
          placeholder="Введите пароль"
        />
      </div>
      
      <button type="submit" class="submit-button">Войти</button>
      
      <p v-if="error" class="error-message">{{ error }}</p>
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
    const password = ref('');
    const error = ref(null);
    const authStore = useAuthStore();
    const router = useRouter();

    const login = async () => {
      try {
        const data = await authService.login(username.value, password.value);
        authStore.login(data.token, { id: data.user_id, username: data.username, email: data.email });
        router.push('/');
      } catch (err) {
        error.value = err.message;
      }
    };

    return {
      username,
      password,
      error,
      login,
    };
  },
};
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 30px;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(0,0,0,0.1);
  font-family: 'Arial', sans-serif;
}

.section-title {
  text-align: center;
  margin-bottom: 20px;
  font-size: 2em;
  color: #34495e;
  font-weight: 600;
}

.login-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 15px;
}

label {
  margin-bottom: 5px;
  font-weight: 600;
  color: #555;
}

input[type="text"],
input[type="password"] {
  width: 100%;
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 1em;
  box-sizing: border-box;
  transition: border-color 0.2s;
}

input:focus {
  border-color: #2980b9;
  outline: none;
}

.submit-button {
  padding: 12px;
  background-color: #2980b9;
  color: #fff;
  border: none;
  border-radius: 10px;
  font-size: 1.1em;
  cursor: pointer;
  margin-top: 20px;
  transition: background-color 0.3s, transform 0.2s;
}

.submit-button:hover {
  background-color: #3498db;
  transform: translateY(-2px);
}

.error-message {
  margin-top: 15px;
  color: red;
  font-weight: 600;
  text-align: center;
}

@media(max-width: 768px) {
  .login-container {
    margin: 20px;
    padding: 20px;
  }
}
</style>