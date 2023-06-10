from flask import Flask
from datetime import date
app = Flask(__name__)
DATABASE = "rateit_db"
TODAY = date.today()
app.secret_key ="ThisIsASecretMat9oulL7ad"