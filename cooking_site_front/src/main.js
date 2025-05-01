import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';
import App from './App.vue';
import HomeView from './views/HomeView.vue';
import RecipeListView from './views/RecipeListView.vue';
import RecipeDetailView from './views/RecipeDetailView.vue';

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/recipes', name: 'recipes', component: RecipeListView },
  { path: '/recipes/:id', name: 'recipe-detail', component: RecipeDetailView, props: true }, 
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

createApp(App).use(router).mount('#app');