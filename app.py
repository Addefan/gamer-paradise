from flask import Flask, render_template
from flask_bootstrap import Bootstrap5

import database as db
from auth import auth
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap5(app)
app.register_blueprint(auth)
db.init_app(app)


@app.route('/')
def main():
    return render_template('base.html')


if __name__ == "__main__":
    app.run(debug=True)
