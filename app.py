#pip install -r requirements.txt

from flask import Flask
from flask_restful import Api
from dieticianApi import morbidity, users, recipe

app = Flask(__name__)
api = Api(app)

api.add_resource(morbidity.MorbidityApi,
                     '/morbidity/MorbidityName=<morbidityName>',
                     '/morbidity/MorbidityTestId=<morbidityTestId>',
                     '/morbidity/MorbidityName=<morbidityName>&MorbidityTestId=<morbidityTestId>',
                     '/morbidity'
                     )

#api.add_resource(users.UsersApi, '/users')
#api.add_resource(recipe.RecipeApi, '/recipes')

if __name__ == '__main__':
    app.run(debug=True)