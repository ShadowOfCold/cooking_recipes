import axios from 'axios';

const API_URL = '/api/accounts/';

const authService = {
    async register(username, email, firstName, lastName, password, password2) {
        try {
            const response = await axios.post(`${API_URL}register/`, {
                username: username,
                email: email,
                first_name: firstName,
                last_name: lastName,
                password: password,
                password2: password2
            });
            return response.data;
        } catch (error) {
            console.error('Registration failed:', error);
            throw error;
        }
    },
    async login(username, password) {
        try {
            const response = await axios.post(`${API_URL}login/`, {
                username: username,
                password: password
            });
            localStorage.setItem('token', response.data.token);
            localStorage.setItem('user_id', response.data.user_id);
            localStorage.setItem('username', response.data.username);
            localStorage.setItem('email', response.data.email);
            return response.data;
        } catch (error) {
            console.error('Login failed:', error);
            throw error;
        }
    },
    logout() {
        localStorage.removeItem('token');
        localStorage.removeItem('user_id');
        localStorage.removeItem('username');
        localStorage.removeItem('email');
    },
    getToken() {
        return localStorage.getItem('token');
    },
    getUserID(){
        return localStorage.getItem('user_id');
    },
    getUsername(){
        return localStorage.getItem('username');
    },
    getEmail(){
        return localStorage.getItem('email');
    }
};

export default authService;