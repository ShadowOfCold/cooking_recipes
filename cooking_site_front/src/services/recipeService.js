import axios from 'axios';

const apiUrl = '/api/recipes';

const recipeService = {
  async getRecommendedRecipes() {
    const response = await axios.get(`${apiUrl}/recommended`);
    return response.data;
  },
};

export default recipeService;