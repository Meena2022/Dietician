# pip install -r requirements.txt
import flask_login
from flask_login import login_user, logout_user, login_required, LoginManager
import flask
from flask import Flask, Blueprint
from flask_restx import Api
from dieticianApi import morbidity, users, recipe
from authentication import DieticianUser
import base64

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


@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        try:
            api_key = base64.b64decode(api_key)
        except TypeError:
            pass
        user_id, password = str(api_key.decode('utf-8')).split(":")
        user = DieticianUser().set(user_id, password)

        if user.is_authenticated():
            return user
    return None


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
