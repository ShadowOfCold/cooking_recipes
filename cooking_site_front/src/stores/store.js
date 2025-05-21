import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', () => {
  const isLoggedIn = ref(false);
  const token = ref(localStorage.getItem('token') || null);
  const user = ref({
    id: localStorage.getItem('user_id') || null,
    username: localStorage.getItem('username') || null,
    email: localStorage.getItem('email') || null
  });

  const setToken = (newToken) => {
    token.value = newToken;
    localStorage.setItem('token', newToken);
  };

  const setUser = (userData) => {
    user.value = userData;
    localStorage.setItem('user_id', userData.id);
    localStorage.setItem('username', userData.username);
    localStorage.setItem('email', userData.email);
  };

  const login = (newToken, userData) => {
    isLoggedIn.value = true;
    setToken(newToken);
    setUser(userData);
  };

  const logout = () => {
    isLoggedIn.value = false;
    token.value = null;
    user.value = { id: null, username: null, email: null };
    localStorage.removeItem('token');
    localStorage.removeItem('user_id');
    localStorage.removeItem('username');
    localStorage.removeItem('email');
  };

  return {
    isLoggedIn,
    token,
    user,
    setToken,
    setUser,
    login,
    logout
  }
})