#pip install -r requirements.txt

from flask import Flask, Blueprint
from flask_restx import Api
from dieticianApi import morbidity, users, recipe

app = Flask(__name__)
blueprint = Blueprint("api", __name__)

api = Api(
    blueprint,
    version="1.0",
    title="Dietician API",
    description="This is the Dietician API created using Flask (Python) by Binary Bombers"
)
app.register_blueprint(blueprint)

api.add_namespace(recipe.api, path="/Recipes")
api.add_namespace(morbidity.api, path="/Morbidity")
api.add_namespace(users.api, path="/Users")


if __name__ == '__main__':
    app.run(debug=True)