from typing import List

class Ingredient(object):
    """
    Basic ingredient object that captures all the details an ingredient must and can have
    """

    def __init__(self, ingredient_id:int, ingredient_name:str, ingredient_quantity:float = 0.0,ingredient_unit:str='default',ingredient_tags:List[str]=None):

        self.ingredient_id = ingredient_id
        self.ingredient_quantity = ingredient_quantity
        self.ingredient_unit = ingredient_unit
        self.ingredient_name = ingredient_name
        self._ingredient_tags = list()
        self.ingredient_tags = ingredient_tags

    @property
    def ingredient_id(self):
        return self._ingredient_id

    @ingredient_id.setter
    def ingredient_id(self, ingredient_id):
        if not type(ingredient_id) == int or ingredient_id < 0:
            raise ValueError(f'Ingredient id ({ingredient_id}) must be a non-negative integer.')
        self._ingredient_id = ingredient_id
        
    @property
    def ingredient_quantity(self):
        return self._ingredient_quantity
    
    @ingredient_quantity.setter
    def ingredient_quantity(self,ingredient_quantity):
        if not type(ingredient_quantity)==float or ingredient_quantity <0:
            raise ValueError(f'Ingredient quantity ({ingredient_quantity}) must be a non-negative float.')
        self._ingredient_quantity = ingredient_quantity
        
    @property
    def ingredient_unit(self):
        return self._ingredient_unit
    
    @ingredient_unit.setter
    def ingredient_unit(self,ingredient_unit):
        if not type(ingredient_unit)==str or not ingredient_unit:
            raise ValueError(f'Ingredient unit ({ingredient_unit}) must be a non-empty string.')
        self._ingredient_unit = ingredient_unit
        
    @property
    def ingredient_name(self):
        return self._ingredient_name

    @ingredient_name.setter
    def ingredient_name(self, ingredient_name):
        if not type(ingredient_name) == str or not ingredient_name:
            raise ValueError(f'Ingredient name ({ingredient_name}) must be a non-empty string.')
        self._ingredient_name = ingredient_name

    @property
    def ingredient_tags(self):
        return self._ingredient_tags

    @ingredient_tags.setter
    def ingredient_tags(self, ingredient_tags):
        intermediate_tags = set()

        if ingredient_tags:
            for ingredient_tag in ingredient_tags:
                if not type(ingredient_tag) == str or not ingredient_tag:
                    raise ValueError(f'Ingredient tag ({ingredient_tag}) must be a non-empty string.')
                intermediate_tags.update([ingredient_tag])

            # Only update the internal tag list if all input tags are valid
            self._ingredient_tags = list(set(self._ingredient_tags + list(intermediate_tags)))

    def update_tags(self, ingredient_tags):
        self.ingredient_tags = ingredient_tags

    def clear_tags(self, ingredient_tags):
        for tag in ingredient_tags:
            if tag in self.ingredient_tags:
                self.ingredient_tags = list(set(self.ingredient_tags).remove(tag))

    def clear_all_tags(self):
        self._ingredient_tags = list()