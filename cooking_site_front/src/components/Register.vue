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
import authService from '../services/authService';

export default {
    data() {
    return {
        username: '',
        email: '',
        firstName: '',
        lastName: '',
        password: '',
        password2: '',
        error: null
    };
    },
    methods: {
    async register() {
        try {
        await authService.register(
            this.username,
            this.email,
            this.firstName,
            this.lastName,
            this.password,
            this.password2
        );
        this.$router.push('/login');
        } catch (error) {
        this.error = error.message;
        }
    }
    }
};
</script>