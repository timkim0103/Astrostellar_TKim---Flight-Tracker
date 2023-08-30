from flask_app import app
from flask_app.controllers import users # importing python files from controllers folder under flask_app
from flask_app.controllers import crafts


if __name__=="__main__":
    app.run(debug=True)