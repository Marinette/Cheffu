import json
import os
import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

import requests
from dotenv import load_dotenv

from ingredient_templates import Ingredient
from recipe_templates import DetailedRecipe
from recipe_templates import Recipe
from spoonacular_wrapper import URL_RECIPES_WITH_INGREDIENTS
from spoonacular_wrapper import URL_RECIPE_BY_ID
from spoonacular_wrapper import search_recipes_from_api
from spoonacular_wrapper import view_recipe_from_api

SAMPLE_RECIPE_LIST_RESPONSE_FILE_PATH = './example_recipe_list_json_response.json'
SAMPLE_DETAILED_RECIPE_RESPONSE_FILE_PATH = './example_detailed_recipe_json_response.json'

class TestSpoonacularWrapper(unittest.TestCase):
    def test_search_recipes_from_api(self):
        """
        Ensure that request.get() is called with the proper URL and parameters, and that a list of DetailedRecipe
        objects are generated from the returned json response

        Contributor: David Zhang
        """
        load_dotenv()
        api_key = os.getenv('SPOONACULAR_API_KEY')
        default_number_returned_recipes = 10

        test_ingredients = [
            Ingredient(ingredient_id=1, ingredient_name='apple', ingredient_tags=['fruit', 'sweet']),
            Ingredient(ingredient_id=10, ingredient_name='flour', ingredient_tags=['starch']),
            Ingredient(ingredient_id=100, ingredient_name='sugar', ingredient_tags=['sweet'])
        ]

        # Set up the mock response
        mock_response = MagicMock()
        mock_response.mock_add_spec(requests.Response)
        mock_response.raise_for_status.side_effect = None
        with open(SAMPLE_RECIPE_LIST_RESPONSE_FILE_PATH, 'r') as filehandler:
            mock_response.json.return_value = json.load(filehandler)

        # Mock out the actual call to the spoonacular api endpoint
        with patch('spoonacular_wrapper.requests.get') as mock_requests_get:
            mock_requests_get.return_value = mock_response

            recipe_list = search_recipes_from_api(test_ingredients)

            # Assert that the proper api endpoint and parameters were used
            mock_requests_get.assert_called_once_with(
                URL_RECIPES_WITH_INGREDIENTS,
                params={
                    'ingredients': [ingredient.ingredient_name for ingredient in test_ingredients],
                    'apiKey': api_key
                }
            )

            self.assertEqual(10, len(recipe_list),
                             'By default, only the {} most relevant recipes are returned by '
                             'Spoonacular API. However, {} DetailedRecipe objects were found '
                             'instead'.format(default_number_returned_recipes, len(recipe_list)))

            # Valid attribute values are asserted prior to being added to the ingredients and recipes classes
            # and are rejected if they do not match with the intended type and contents
            for recipe in recipe_list:
                self.assertEqual(DetailedRecipe, type(recipe),
                                 '{} is not of type {}'.format(recipe, DetailedRecipe))

    def test_view_recipe_from_api(self):
        """
        Ensure that request.get() is called with the proper URL and parameters, and that a correctly populated
        DetailedRecipe object is returned

        Contributor: David Zhang
        """
        load_dotenv()
        api_key = os.getenv('SPOONACULAR_API_KEY')

        test_recipe_id = 987595

        # ingredient_id may not be unique due to different variants of ingredients. Key by id and name
        expected_ingredient_list = [
            Ingredient(
                ingredient_id=11216,
                ingredient_name='ginger',
                ingredient_quantity=60.0,
                ingredient_quantity_units='ml'
            ).__dict__,
            Ingredient(
                ingredient_id=9003,
                ingredient_name='apple',
                ingredient_quantity=30.0,
                ingredient_quantity_units='ml'
            ).__dict__,
            Ingredient(
                ingredient_id=9003,
                ingredient_name='apples',
                ingredient_quantity=1.0,
                ingredient_quantity_units='serving'
            ).__dict__
        ]

        # Set up the mock response
        mock_response = MagicMock()
        mock_response.mock_add_spec(requests.Response)
        mock_response.raise_for_status.side_effect = None
        with open(SAMPLE_DETAILED_RECIPE_RESPONSE_FILE_PATH, 'r') as filehandler:
            mock_response.json.return_value = json.load(filehandler)

        # Mock out the actual call to the spoonacular api endpoint
        with patch('spoonacular_wrapper.requests.get') as mock_requests_get:
            mock_requests_get.return_value = mock_response

            detailed_recipe = view_recipe_from_api(test_recipe_id)

            # Assert that the proper api endpoint and parameters were used
            mock_requests_get.assert_called_once_with(
                URL_RECIPE_BY_ID.format(recipe_id=987595),
                params={
                    'includeNutrition': True,
                    'apiKey': api_key
                }
            )

            # Assert that each attribute is present as expected. Ignore recipe_description as it allows free text form.
            self.assertEqual(987595, detailed_recipe.recipe_id)
            self.assertEqual('Apple Ginger Kombucha Cocktail', detailed_recipe.recipe_name)
            self.assertEqual('https://api.spoonacular.com/recipes/987595/information', detailed_recipe.recipe_url)
            self.assertEqual('https://spoonacular.com/recipeImages/987595-556x370.jpg', detailed_recipe.recipe_image_url)
            self.assertEqual({'paleolithic', 'gluten free', 'vegan', 'dairy free', 'primal', 'lacto ovo vegetarian'},
                             set(detailed_recipe.recipe_tags))
            self.assertEqual(['Combine ingredients in a glass and stir to mix.',
                              'Garnish with thinly sliced apples if desired.'],
                             detailed_recipe.recipe_instructions)
            self.assertEqual(2.0, detailed_recipe.recipe_preparation_time)

            for ingredient in detailed_recipe.recipe_ingredients:
                self.assertIn(ingredient.__dict__, expected_ingredient_list)

    #def test_find_recipes_with_ingredients(self):
    #TODO: Add unittest to test database hit/miss interactions


if __name__ == '__main__':
    unittest.main()
