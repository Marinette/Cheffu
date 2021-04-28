import csv
import json
import os

import requests
from dotenv import load_dotenv
from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
from flask_cors import cross_origin

from backend.ingredient_templates import Ingredient
from backend.spoonacular_wrapper import find_recipes_with_ingredients
from backend.spoonacular_wrapper import view_recipe_from_api

from flask import send_from_directory

load_dotenv()
SPOONACULAR_API_KEY = os.getenv('SPOONACULAR_API_KEY')
SPOONACULAR_API_KEY = "7ce9ace996e64fe88f88d96b77422eac"

app = Flask(__name__, static_folder='client/build', template_folder='client/build', static_url_path='')
CORS(app, support_credentials=True)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
   if path != "" and os.path.exists(app.static_folder + '/' + path):
      return send_from_directory(app.static_folder, path)
   else:
      return send_from_directory(app.static_folder, 'index.html')

@app.errorhandler(404)
def handle_404(e):
    return send_from_directory(app.static_folder, "index.html")

# @app.route('/', methods=['GET'])
# @cross_origin(support_credentials=True)
# def home():
#     #TODO: setup home page
#     return send_from_directory(app.static_folder, 'index.html')

# Route to convert units for a specific ingredient 
@app.route('/api/convert_units', methods=['GET'])
@cross_origin(support_credentials=True)
def convert_units():
   ingredientName = request.args.get('ingredientName')
   sourceAmount = request.args.get('sourceAmount')
   sourceUnit = request.args.get('sourceUnit')
   targetUnit = request.args.get('targetUnit')

   URL = 'https://api.spoonacular.com/recipes/convert'

   PARAMS = {
      'ingredientName': ingredientName,
      'sourceAmount': sourceAmount,
      'sourceUnit': sourceUnit,
      'targetUnit': targetUnit,
      'apiKey': SPOONACULAR_API_KEY
   }

   res = requests.get(url = URL, params = PARAMS)
   data = res.json()

   return jsonify(data)


# Route to filter by calories
@app.route('/api/filter_by_calories', methods=['GET'])
@cross_origin(support_credentials=True)
def filter_calories():
   minCalories = request.args.get('minCalories')
   maxCalories = request.args.get('maxCalories')
   recipeIdList = request.args.get('recipeIdList')

   URL = 'https://api.spoonacular.com/recipes/findByNutrients'

   PARAMS = {
      'minCalories': minCalories,
      'maxCalories': maxCalories,
      'apiKey': SPOONACULAR_API_KEY
   }

   res = requests.get(url = URL, params = PARAMS)
   data = res.json()

   # Output is the intersection of the list of recipes from frontend (recipeIdList)
   # and the recipes that meet the calorie requirement (data)
   out = []
   for recipeId in data:
      if str(recipeId['id']) in recipeIdList:
         out.append(recipeId) 

   return jsonify(out)


# Route to filter by macros
@app.route('/api/filter_by_macros', methods=['GET'])
@cross_origin(support_credentials=True)
def filter_macros():
   minCarbs = request.args.get('minCarbs')
   maxCarbs = request.args.get('maxCarbs')
   minProtein = request.args.get('minProtein')
   maxProtein = request.args.get('maxProtein')
   minFat = request.args.get('minFat')
   maxFat = request.args.get('maxFat')
   recipeIdList = request.args.get('recipeIdList')

   URL = 'https://api.spoonacular.com/recipes/findByNutrients'

   PARAMS = {
      'minCarbs': minCarbs,
      'maxCarbs': maxCarbs,
      'minProtein': minProtein,
      'maxProtein': maxProtein,
      'minFat': minFat,
      'maxFat': maxFat,
      'apiKey': SPOONACULAR_API_KEY
   }

   res = requests.get(url = URL, params = PARAMS)
   data = res.json()

   # Output is the intersection of the list of recipes from frontend (recipeIdList)
   # and the recipes that meet the Macro requirement (data)
   out = []
   for recipeId in data:
      if str(recipeId['id']) in recipeIdList:
         out.append(recipeId) 

   return jsonify(out)


# Route to get list of recipes 
@app.route('/api/get_ingredients', methods=['GET'])
@cross_origin(support_credentials=True)
def get_ingredients():
       
   data_list = []
   with open('cache/common_ingredients.csv') as f:
      csvReader = csv.DictReader(f, delimiter=';')
      for row in csvReader:
         data_list.append(row)

   return jsonify(data_list)


# Route to get list of recipes from list of ingredients 
@app.route('/api/search', methods=['POST'])
@cross_origin(support_credentials=True)
def search_recipes():
   ingredients = request.get_json()
    
   print("List of ingredients:",ingredients['ingredients'])
   listOfIngredients = []
   for item in ingredients['ingredients']:
      newIngredient = Ingredient(int(item['ingredientID']), item['ingredientName'])
      listOfIngredients.append(newIngredient)
   recipes = find_recipes_with_ingredients(listOfIngredients)
   
   recipesJson = json.dumps(recipes, default=(lambda obj: obj.__dict__))

   return jsonify(json.loads(recipesJson))


# Route to get detailed recipe from its recipeid
@app.route('/api/recipe_details', methods=['GET'])
@cross_origin(support_credentials=True)
def recipe_details():
   recipeId = request.args.get('recipeid')

   recipeDetail = view_recipe_from_api(recipeId)

   recipeDetailJson = json.dumps(recipeDetail, default=(lambda obj: obj.__dict__))

   return jsonify(json.loads(recipeDetailJson))


if __name__ == "__main__":
    app.run(debug=True)