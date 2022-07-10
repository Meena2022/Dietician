#pip install -r requirements.txt

from flask import Flask
from flask_restful import Api
from dieticianApi import morbidity, users, recipe

app = Flask(__name__)
api = Api(app)

api.add_resource(morbidity.MorbidityApi,
                     '/Morbidity/MorbidityName=<morbidityName>',
                     '/Morbidity/MorbidityTestId=<morbidityTestId>',
                     '/Morbidity/MorbidityName=<morbidityName>&MorbidityTestId=<morbidityTestId>',
                     '/Morbidity'
                     )

api.add_resource(recipe.RecipeApi,
                    '/Recipes/RecipeFoodCategory=<recipeFoodCategory>',
                    '/Recipes/RecipeType=<recipeType>',
                    '/Recipes/RecipeIngredient=<recipeIngredient>',
                    '/Recipes/RecipeNutrient=<recipeNutrient>',
                    '/Recipes'
                     )
api.add_resource(users.UsersApi,
                 '/users/FirstName=<FirstName>',
                 '/users/Email=<Email>',
                 '/users/Contact=<Contact>',
                 '/users/UserType=<UserType>',
                 '/users/DieticianId=<DieticianId>',
                 '/users'
                 )

if __name__ == '__main__':
    app.run(debug=True)