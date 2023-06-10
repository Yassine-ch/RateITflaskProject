from flask_app import app
from flask_app.controllers import users, sectors, reviews, companies


if __name__ == "__main__":
    app.run(debug=True)