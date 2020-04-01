import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
from flask import Flask

#client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['projet_flask']

# remplir fake user sur la db "projet_flask"
def database_constructor(user):
    userbase = db.user_collection
    userbase.insert_one(user).inserted_id
    db.list_collection_names()

# fonction qui ajoute nouvel user via à la base projet_flask via le formulaire
def feed_data(text_username, text_prenom, text_nom,text_genre):
    user = {"nom": text_nom,
            "prenom":text_prenom,
            "gender":text_genre,
            "username":text_username,
            }
    userbase = db.user_collection
    userbase.insert_one(user).inserted_id
    db.list_collection_names()

# fonction qui permet de vérifier si le pseudo username existe déja dans la db
def check_username(text_username):
    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb://localhost:27017/projet_flask"
    mongo = PyMongo(app)
    user = mongo.db.user_collection.find({'username':text_username})
    return list(user)

#fonction qui liste tout les pseudo de la db
def liste_username():
    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb://localhost:27017/projet_flask"
    mongo = PyMongo(app)
    data_user = mongo.db.user_collection.find()
    liste = list(data_user)
    liste_username =[]
    for user in liste:
        liste_username.append(user['username'])
    return liste_username

def kill_database():
    client.drop_database('projet_flask')