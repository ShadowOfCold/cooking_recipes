import axios from 'axios';

const API_URL = '/api/recipes/';

const recipeService = {
  async getRecipes() {
    try {
      const response = await axios.get(API_URL);
      return response.data;
    } catch (error) {
      console.error('Error fetching recipes:', error);
      throw error;
    }
  },
  async getRecipe(id) {
    try {
      const response = await axios.get(`${API_URL}${id}/`);
      return response.data;
    } catch (error) {
      console.error('Error fetching recipe:', error);
      throw error;
    }
  },
  async getRecommendedRecipes() {
    try {
      const response = await axios.get(`${API_URL}recommended`);
      return response.data;
    } catch (error) {
      console.error('Error fetching recommended recipes:', error);
      throw error;
    }
  }
};

export default recipeService;