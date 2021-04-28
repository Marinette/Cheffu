from typing import List

from backend.ingredient_templates import Ingredient

class Recipe(object):
    """
    Basic recipe object that captures all the details a recipe must and can have
    """

    def __init__(self, recipe_id:int, recipe_name:str, recipe_url:str, recipe_image_url:str=None,
                 recipe_description:str=None, recipe_rating:float=None, recipe_tags:List[str]=None):
        self.recipe_id = recipe_id
        self.recipe_name = recipe_name
        self.recipe_url = recipe_url
        self.recipe_image_url = recipe_image_url
        self.recipe_description = recipe_description
        self.recipe_rating = recipe_rating
        self._recipe_tags = list()
        self.recipe_tags = recipe_tags

    @property
    def recipe_id(self):
        return self._recipe_id

    @recipe_id.setter
    def recipe_id(self, recipe_id):
        if not type(recipe_id) == int or recipe_id < 0:
            raise ValueError(f'Recipe id ({recipe_id}) must be a non-negative integer.')
        self._recipe_id = recipe_id

    @property
    def recipe_name(self):
        return self._recipe_name

    @recipe_name.setter
    def recipe_name(self, recipe_name):
        if not type(recipe_name) == str or not recipe_name:
            raise ValueError(f'Recipe name ({recipe_name}) must be a non-empty string.')
        self._recipe_name = recipe_name

    @property
    def recipe_url(self):
        return self._recipe_url

    @recipe_url.setter
    def recipe_url(self, recipe_url):
        if not type(recipe_url) == str or not recipe_url:
            raise ValueError(f'Recipe url ({recipe_url}) must be a non-empty string.')
        self._recipe_url = recipe_url

    @property
    def recipe_image_url(self):
        return self._recipe_image_url

    @recipe_image_url.setter
    def recipe_image_url(self, recipe_image_url):
        if recipe_image_url is not None and (not type(recipe_image_url) == str or not recipe_image_url):
            raise ValueError(f'Recipe image url ({recipe_image_url}) must be a non-empty string or Nonetype.')
        self._recipe_image_url = recipe_image_url

    @property
    def recipe_description(self):
        return self._recipe_url

    @recipe_description.setter
    def recipe_description(self, recipe_description):
        if recipe_description is not None and (not type(recipe_description) == str or not recipe_description):
            raise ValueError(f'Recipe description ({recipe_description}) must be a non-empty string or Nonetype.')
        self._recipe_description = recipe_description

    @property
    def recipe_rating(self):
        return self._recipe_url

    @recipe_rating.setter
    def recipe_rating(self, recipe_rating):
        if recipe_rating is not None and (not type(recipe_rating) == str or not recipe_rating):
            raise ValueError(f'Recipe rating ({recipe_rating}) must be a non-empty string or Nonetype.')
        self._recipe_rating = recipe_rating

    @property
    def recipe_tags(self):
        return self._recipe_tags

    @recipe_tags.setter
    def recipe_tags(self, recipe_tags):
        intermediate_tags = set()

        if recipe_tags:
            for recipe_tag in recipe_tags:
                if not type(recipe_tag) == str or not recipe_tag:
                    raise ValueError(f'Recipe tag ({recipe_tag}) must be a non-empty string.')
                intermediate_tags.update([recipe_tag])

            # Only update the internal tag list if all input tags are valid
            self._recipe_tags = list(set(self._recipe_tags + list(intermediate_tags)))

    def update_tags(self, recipe_tags):
        self.recipe_tags = recipe_tags

    def clear_tags(self, recipe_tags):
        for tag in recipe_tags:
            if tag in self.recipe_tags:
                self.recipe_tags.remove(tag)

    def clear_all_tags(self):
        self._recipe_tags = list()


class DetailedRecipe(Recipe):
    """
    Detailed recipe object that extends Recipe and adds several extra attributes and properties
    """
    def __init__(self, recipe_id:int, recipe_name:str, recipe_url:str, recipe_ingredients:List[Ingredient], recipe_servings=None,
                 recipe_instructions:List[str]=None, recipe_preparation_time:float=None, recipe_cooking_time:float=None,
                 recipe_image_url:str=None, recipe_description:str=None, recipe_rating:float=None,
                 recipe_tags:List[str]=None):
        super(DetailedRecipe, self).__init__(recipe_id, recipe_name, recipe_url, recipe_image_url, recipe_description,
                                             recipe_rating, recipe_tags)

        self._recipe_ingredients = list()
        self.recipe_ingredients = recipe_ingredients

        self.recipe_servings = recipe_servings
        
        self._recipe_instructions = []
        self.recipe_instructions = recipe_instructions

        self.recipe_preparation_time = recipe_preparation_time
        self.recipe_cooking_time = recipe_cooking_time

    @property
    def recipe_ingredients(self):
        return self._recipe_ingredients

    @recipe_ingredients.setter
    def recipe_ingredients(self, recipe_ingredients):
        intermediate_ingredients = set()

        for ingredient in recipe_ingredients:
            if not isinstance(ingredient, Ingredient):
                raise ValueError(f'Ingredient ({ingredient}) is invalid or malformed.')
            intermediate_ingredients.update([ingredient])

        # Only update the internal ingredient list if all input ingredients are valid
        self._recipe_ingredients = list(set(self._recipe_ingredients + list(intermediate_ingredients)))

    def update_ingredients(self, recipe_ingredients):
        self.recipe_ingredients = recipe_ingredients

    def clear_ingredients(self, recipe_ingredients):
        for ingredient in recipe_ingredients:
            if ingredient in self.recipe_ingredients:
                self.recipe_ingredients.remove(ingredient)

    def clear_all_ingredients(self):
        self._recipe_ingredients = list()

    @property
    def recipe_instructions(self):
        return self._recipe_instructions

    @recipe_instructions.setter
    def recipe_instructions(self, recipe_instructions):
        if recipe_instructions is not None:
            intermediate_instructions = []

            for instruction in recipe_instructions:
                if not type(instruction) == str or not instruction:
                    raise ValueError(f'Recipe instructions are malformed. ({recipe_instructions})')
                intermediate_instructions.append(instruction)

            # Only update the internal instruction list if all input instructions are valid
            self._recipe_instructions = intermediate_instructions
        elif not self._recipe_instructions:
            self._recipe_instructions = []

    def rewrite_instructions(self, recipe_instructions):
        self.recipe_instructions = recipe_instructions

    def clear_recipe_instructions(self):
        self._recipe_ingredients = []
        
    @property 
    def recipe_servings(self):
        return self._recipe_servings
    
    @recipe_servings.setter
    def recipe_servings(self,recipe_servings):
        if not type(recipe_servings == int or not recipe_servings):
            raise ValueError(f'Recipe servings ({recipe_servings}) must be a non-empty int.')
        self._recipe_servings = recipe_servings
        
    @property
    def recipe_preparation_time(self):
        return self._recipe_preparation_time

    @recipe_preparation_time.setter
    def recipe_preparation_time(self, recipe_preparation_time):
        if recipe_preparation_time is not None:
            if not type(recipe_preparation_time) in [float, int] or recipe_preparation_time < 0:
                raise ValueError(f'Recipe preparation time ({recipe_preparation_time}) must be a non-negative number.')
            else:
                self._recipe_preparation_time = float(recipe_preparation_time)

    @property
    def recipe_cooking_time(self):
        return self._recipe_cooking_time

    @recipe_cooking_time.setter
    def recipe_cooking_time(self, recipe_cooking_time):
        if recipe_cooking_time is not None:
            if not type(recipe_cooking_time) in [float, int] or recipe_cooking_time < 0:
                raise ValueError(f'Recipe cooking time ({recipe_cooking_time}) must be a non-negative number.')
            else:
                self._recipe_cooking_time = float(recipe_cooking_time)