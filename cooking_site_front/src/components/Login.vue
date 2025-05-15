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
import authService from '../services/authService';

export default {
    data() {
    return {
        username: '',
        password: '',
        error: null
    };
    },
    methods: {
    async login() {
        try {
        await authService.login(this.username, this.password);
        this.$router.push('/');
        } catch (error) {
        this.error = error.message;
        }
    }
    }
};
</script>
