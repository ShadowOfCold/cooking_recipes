<template>
    <div>
    <h2>Вход</h2>
    <form @submit.prevent="login">
        <div>
        <label for="username">Имя пользователя:</label>
        <input type="text" id="username" v-model="username" required>
        </div>
        <div>
        <label for="password">Пароль:</label>
        <input type="password" id="password" v-model="password" required>
        </div>
        <button type="submit">Войти</button>
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
        login
    };
    }
};
</script>