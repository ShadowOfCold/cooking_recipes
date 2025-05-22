<template>
  <div class="registration-form-container">
    <h2>Регистрация</h2>
    <form @submit.prevent="register" class="register-form">
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
        <label for="email">Email</label>
        <input
          type="email"
          id="email"
          v-model="email"
          required
          placeholder="Введите email"
        />
      </div>
      
      <div class="form-row">
        <div class="form-group half">
          <label for="firstName">Имя</label>
          <input
            type="text"
            id="firstName"
            v-model="firstName"
            required
            placeholder="Ваше имя"
          />
        </div>
        <div class="form-group half">
          <label for="lastName">Фамилия</label>
          <input
            type="text"
            id="lastName"
            v-model="lastName"
            required
            placeholder="Ваша фамилия"
          />
        </div>
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
      
      <div class="form-group">
        <label for="password2">Подтвердите пароль</label>
        <input
          type="password"
          id="password2"
          v-model="password2"
          required
          placeholder="Повторите пароль"
        />
      </div>
      
      <button type="submit" class="submit-button">Зарегистрироваться</button>
      
      <p v-if="error" class="error-message">{{ error }}</p>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue';
import authService from '../services/authService';
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
    const router = useRouter();

    const register = async () => {
      try {
        await authService.register(
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

<style scoped>
.registration-form-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 30px;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(0,0,0,0.1);
}

h2 {
  text-align: center;
  margin-bottom: 20px;
  font-family: 'Arial', sans-serif;
  font-weight: 600;
  color: #34495e;
}

.register-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 15px;
}

.form-row {
  display: flex;
  gap: 10px;
}

.half {
  flex: 1;
}

label {
  margin-bottom: 5px;
  font-weight: 600;
  color: #555;
}

input[type="text"],
input[type="email"],
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
  border-color: #4CAF50;
  outline: none;
}

.submit-button {
  padding: 12px;
  background-color: #4CAF50;
  color: #fff;
  border: none;
  border-radius: 10px;
  font-size: 1.1em;
  cursor: pointer;
  margin-top: 20px;
  transition: background-color 0.3s, transform 0.2s;
}

.submit-button:hover {
  background-color: #4CAF50;
  transform: translateY(-2px);
}

.error-message {
  color: red;
  font-weight: 600;
  margin-top: 15px;
  text-align: center;
}

@media (max-width: 768px) {
  .form-row {
    flex-direction: column;
  }
}
</style>