from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
import bdd # hand made
import json
import pandas as pd
import numpy as np
import os
import psycopg2
import base64
from PIL import Image
from io import BytesIO


cwd = os.getcwd()



try:
    app = Flask(__name__)

    # remplir fake user sur la db "projet_flask"
    with open("./static/data.json", "r") as read_file:
        data = json.load(read_file)

    for user in data:
        bdd.database_constructor(user)



    # exercice 1 & 2 
    @app.route("/")
    def hello():
        return render_template("home.html", message = "Hello World!")

    # exercice 3
    @app.route("/exo3")
    def exo_3():
        return render_template("exo_3.html")

    # exercice 4
    @app.route("/exo4")
    def exo_4():
        return render_template("exo_4_formulaire.html")

    @app.route('/exo4', methods=['POST'])
    def text_box():
        text_username = request.form['username'].lower()
        text_prenom = request.form['prenom'].lower()
        text_nom = request.form['nom'].lower()
        text_sexe = request.form['sexe'].lower()
        if text_sexe == "HOMME":
            text_genre = "Male"
        else:
            text_genre = "Female"
        return render_template("exo_4_welcome_page.html", username = text_username, prenom = text_prenom, nom = text_nom, genre = text_genre )

    # exercice 5
    @app.route("/exo5")
    def exo_5():
        return render_template("exo_5_formulaire.html")

    @app.route('/exo5', methods=['POST'])
    def text_box_bdd():
        text_username = request.form['username'].lower()
        text_prenom = request.form['prenom'].lower()
        text_nom = request.form['nom'].lower()
        text_sexe = request.form['sexe'].lower()

        #genre homme ou femme
        if text_sexe == "HOMME":
            text_genre = "Monsieur"
        else:
            text_genre = "Madame"

        #test pseudo existe deja        
        user_found = bdd.check_username(text_username)
        if len(user_found) < 1 :
            bdd.feed_data(text_username, text_prenom, text_nom,text_genre)
        else:
            for k,v in user_found[0].items():
                if k == "username":
                    username_found = v
            return render_template("exo_5_formulaire.html", control = f"{username_found} existe déjà ! ")
        return render_template("exo_5_welcome_page.html", username = text_username, prenom = text_prenom, nom = text_nom, genre = text_genre)

    # exercice 6
    @app.route('/exo6')
    def exo_6():
        liste = bdd.liste_username()
        return render_template("exo_6.html", liste_user = liste)
        
    # exercice 7
    @app.route('/exo7')
    def exo_7():
        return render_template("exo_7.html")

    @app.route('/exo7', methods=['POST'])
    def input_file():
        file = request.form['myfile']
        data = pd.read_csv(f"./static/{file}", sep ="[,;:|_]")
        stats = data.describe().to_html()
        return render_template("exo_7_dataframe.html", dataframe = stats, titre_dataframe = file )

    # exercice 8 : desssiner chiffre etr le faire deviner par algo
    @app.route('/exo8', methods=['GET', 'POST'])
    def paintapp():
        if request.method == 'GET':
            return render_template("paint.html")
        if request.method == 'POST':
            filename = request.form['save_fname']
            data = request.form['save_cdata']
            canvas_image = request.form['save_image']
            print(f"test -----------------------------------> {canvas_image}")
            im = Image.open(BytesIO(base64.b64decode(canvas_image[21:])))
            im.save(f"{filename}.png", 'PNG')
            #conn.commit()
            #conn.close()
            return render_template("home.html" )        
            
            
    @app.route('/save', methods=['GET', 'POST'])
    def save():
        conn = psycopg2.connect(database="paintmyown", user="nidhin")
        cur = conn.cursor()
        cur.execute("SELECT id, name, data, canvas_image from files")
        files = cur.fetchall()
        conn.close()
        return render_template("home.html" )
        


    if __name__ == "__main__":
        app.run(debug = True)   

# forcer procédure de fin, effacer la base de donnée NoSQL en quittant le programme
finally:
    bdd.kill_database()        
