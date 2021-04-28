import os
from copy import deepcopy
from typing import Any
from typing import Dict
from typing import List
from warnings import warn

import requests
from dotenv import load_dotenv

from backend.ingredient_templates import Ingredient
from backend.recipe_templates import DetailedRecipe
from backend.recipe_templates import Recipe

load_dotenv()
SPOONACULAR_API_KEY = os.getenv('SPOONACULAR_API_KEY')

API_KEY = 'apiKey'
INGREDIENTS = 'ingredients'
INCLUDE_NUTRITION = 'includeNutrition'

URL_RECIPES_WITH_INGREDIENTS = 'https://api.spoonacular.com/recipes/findByIngredients'
URL_RECIPE_BY_ID = 'https://api.spoonacular.com/recipes/{recipe_id}/information'

QUERY_RECIPES_WITH_INGREDIENTS = {
    INGREDIENTS: [],
    API_KEY: SPOONACULAR_API_KEY
}
QUERY_RECIPE_BY_ID = {
    INCLUDE_NUTRITION: True,
    API_KEY: SPOONACULAR_API_KEY
}


def find_recipes_with_ingredients(ingredients:List[Ingredient]) -> List[DetailedRecipe]:
    """
    Finds recipes that use or are related to the list of ingredients provided
    :param List[Ingredient] ingredients: A list of ingredients to be searched on
    :return: The recipes that matched with the ingredients provided
    :rtype: List[Recipe]
    """

    recipes = find_recipes_from_cache(ingredients)

    if not recipes:  # database miss
        recipes = search_recipes_from_api(ingredients)

    return recipes


def find_recipes_from_cache(ingredients:List[Ingredient]) -> List[DetailedRecipe]:
    """
    Attempts to search for cached recipes related to the ingredients in the database
    :param List[Ingredient] ingredients: A lsit of ingredients to be searched on
    :return: The recipes that matched with the ingredients provided
    :rtype: List[DetailedRecipe]
    """
    warn('Database search not currently implemented')
    #TODO: implement a cache/database retrieval
    return []


def search_recipes_from_api(ingredients:List[Ingredient]) -> List[DetailedRecipe]:
    """
    Given a list of ingredients, query the API to determine recipes that use or are related to the ingredients
    :param List[Ingredient] ingredients: A list of ingredients to be searched on
    :return: The recipes that matched with the ingredients provided
    :rtype: List[DetailedRecipe]
    """
    query = deepcopy(QUERY_RECIPES_WITH_INGREDIENTS)

    for ingredient in ingredients:
        query[INGREDIENTS].append(ingredient.ingredient_name)

    #print(query)

    response = requests.get(URL_RECIPES_WITH_INGREDIENTS, params=query)
    response.raise_for_status()
    response_data = response.json()

    #print(response_data)

    matching_recipes = _get_recipes_list_from_json(response_data)

    return matching_recipes


def _get_recipes_list_from_json(json_object:List[Dict[str, Any]]) -> List[DetailedRecipe]:
    """
    Extracts a list of recipes with some basic details prefilled from a json response dictionary
    :param List[Dict[str, Any]] json_object:
    :return: A list of the recipes provided
    :rtype: List[DetailedRecipe]
    """
    recipe_list = []

    for recipe_json_entry in json_object:
        # Get all the ingredient names that are used in the recipe
        recipe_ingredients = [
            Ingredient(
                ingredient_id=ingredient_json.get('id'),
                ingredient_name=ingredient_json.get('name'),
                ingredient_quantity=ingredient_json.get('amount')
            )
            for ingredient_json in recipe_json_entry.get('usedIngredients', {})
        ]
        recipe_ingredients.extend([
            Ingredient(
                ingredient_id=ingredient_json.get('id'),
                ingredient_name=ingredient_json.get('name'),
                ingredient_quantity=ingredient_json.get('amount')
            )
            for ingredient_json in recipe_json_entry.get('missedIngredients', {})
        ])

        recipe_list.append(DetailedRecipe(
            recipe_id=recipe_json_entry.get('id'),
            recipe_name=recipe_json_entry.get('title'),
            recipe_url=URL_RECIPE_BY_ID.format(recipe_id=recipe_json_entry.get('id')),
            recipe_ingredients=recipe_ingredients,
            recipe_image_url=recipe_json_entry.get('image')
        ))

    return recipe_list


def view_recipe_from_api(recipe_id:int) -> DetailedRecipe:
    """
    Given a recipe_id, query the API to determine the recipe details
    :param int recipe_id: The recipe id to look up the details of
    :return: The detailed recipe with all relevant fields
    :rtype: DetailedRecipe
    """
    response = requests.get(URL_RECIPE_BY_ID.format(recipe_id=recipe_id), params=QUERY_RECIPE_BY_ID)
    response.raise_for_status()
    response_data = response.json()

    recipe_details = _get_recipe_details_from_json(response_data)

    return recipe_details


def _get_recipe_details_from_json(json_object:Dict[str, Any]) -> DetailedRecipe:
    """
    Extracts the relevant recipe information from a json response dictionary
    :param Dict[str, Any] json_object: The json response to deduce DetailedRecipe attributes from
    :return: A DetailedRecipe object that captures all the relevant recipe details
    :rtype: DetailedRecipe
    """

    recipe_ingredients =  [
        Ingredient(
            ingredient_id=ingredient_json.get('id'),
            ingredient_name=ingredient_json.get('name'),
            ingredient_quantity=ingredient_json.get('amount'),
            ingredient_unit = ingredient_json.get("unit")
        )
        for ingredient_json in json_object.get('extendedIngredients', {})
    ]

    detailed_recipe = DetailedRecipe(
        recipe_id=json_object.get('id'),
        recipe_name=json_object.get('title'),
        recipe_url = URL_RECIPE_BY_ID.format(recipe_id=json_object.get('id')),
        recipe_ingredients=recipe_ingredients,
        recipe_instructions=json_object.get('instructions').split('\n') if json_object.get('instructions') else [],
        recipe_preparation_time=json_object.get('readyInMinutes'),
        recipe_image_url=json_object.get('image'),
        recipe_description=json_object.get('summary'),
        recipe_tags=json_object.get('diets'),
        recipe_servings = json_object.get('servings')

    )

    return detailed_recipe


# -------------- TESTING CODE ---------------
#
#
#def random_ingredients():
#    apple = Ingredient(1, 'apple', ['fruit', 'sweet', 'sugar'])
#    flour = Ingredient(124, 'flour', ['pantry'])
#    sugar = Ingredient(9832, 'sugar', ['sweet', 'sugar'])
#
#    ingredient_list = [apple, flour, sugar]
#
#    recipe_list = find_recipes_with_ingredients(ingredient_list)
#
#    print(recipe_list)
#
#def random_recipe():
#    recipe_id = 987595
#
#    #detailed_recipe = view_recipe_from_api(recipe=Recipe(recipe_id=recipe_id, recipe_name='Apple Ginger Kombucha Cocktail', recipe_url=URL_RECIPE_BY_ID.format(recipe_id=recipe_id)))
#    detailed_recipe = view_recipe_from_api(recipe_id)
#
#    print(detailed_recipe.__dict__)
#    for ingredient in detailed_recipe.recipe_ingredients:
#        print(ingredient.__dict__)
#
#
#if __name__ == '__main__':
##    #random_ingredients()
#    #random_recipe()
#    pass
