# pip install -r requirements.txt
import flask_login
from flask_login import login_user, logout_user, login_required, LoginManager
import flask

from flask import Flask, Blueprint
from flask_restx import Api
from dieticianApi import morbidity, users, recipe
from authentication import DieticianUser

app = Flask(__name__)
blueprint = Blueprint("api", __name__,
    url_prefix='/api')

api = Api(
    blueprint,
    version="1.0",
    title="DieticianAPI",
    description="This is the Dietician API created using Flask (Python) by Binary Bombers",
)
app.register_blueprint(blueprint)
api.add_namespace(recipe.api, path="/Recipes")
api.add_namespace(morbidity.api, path="/Morbidity")
api.add_namespace(users.api, path="/Users")

app.secret_key = 'mysecretkey'
login_manager = LoginManager(app)
login_manager.init_app(app)

@app.login_manager.user_loader
def load_user(user_id):
    user = DieticianUser().getUser(user_id)
    return user


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return flask.redirect("/")


@app.route('/', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        form_data = flask.request.form
        user = DieticianUser().set(form_data['user_id'], form_data['password'])
        if user is not None:
            login_user(user)
            flask.flash('Logged in successfully.')
            next = flask.request.args.get('next')
            return flask.redirect(next or '/api')
        return flask.render_template('login.html')
    return flask.render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
