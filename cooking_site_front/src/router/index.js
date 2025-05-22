import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import RecipeDetail from '../components/RecipeDetail.vue';
import Register from '../components/Register.vue';
import Login from '../components/Login.vue';
import RecipeForm from '../components/RecipeForm.vue';
import RecipeList from '../components/RecipeList.vue';
import EditRecipe from '../components/EditRecipe.vue';
import MyRecipes from '../components/MyRecipes.vue';
import { useAuthStore } from '../stores/store';

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/recipes',
    name: 'recipes',
    component: RecipeList
  },
  {
    path: '/recipes/:id',
    name: 'recipeDetail',
    component: RecipeDetail,
    props: true
  },
  {
    path: '/my-recipes',
    name: 'MyRecipes',
    component: MyRecipes,
  },
  {
    path: '/my-recipes/:id/edit',
    name: 'EditRecipe',
    component: EditRecipe,
    props: true,
  },
  {
    path: '/register',
    name: 'register',
    component: Register
  },
  {
    path: '/login',
    name: 'login',
    component: Login
  },
  {
    path: '/recipes/create',
    name: 'recipeCreate',
    component: RecipeForm,
    meta: { requiresAuth: true }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    next('/login');
  } else {
    next();
  }
});

export default router;