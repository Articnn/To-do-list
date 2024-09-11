from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)

with app.app_context():
    db.create_all()
    print("Database tables created")
    
    
''''
Esto es basicamente como el de app.py pero lo cree
por que no funcionaba la db entonces con esto podia ver si se generaba o no
aunqye creo que la manual fue la efectiva vaya...

'''
