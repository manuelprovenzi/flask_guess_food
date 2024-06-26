import json
from flask import Flask, render_template, request, make_response
from food_api import FoodAPI
from image import Image
import os
import random
import hashlib
from databaseManager import DatabaseManager
import time


class PageManager:

    def __init__(self, app, db_manager):
        self.app = app
        self.db_manager = db_manager
        self.cibo_vincente = None
        self.secondi_totali_timer = 300

        @self.app.route('/')
        def index():
            if 'username' in request.cookies:
                return render_template('index.html')
            else:
                return render_template('login.html',bool_login=True)

        @self.app.route('/game', methods=['GET', 'POST'])
        def game():
            if request.method == 'GET':
                timer = request.args.get('timer')
                if timer=="terminato":
                    self.db_manager.update_user_timer(request.cookies.get('id'), -1)
                    self.db_manager.set_user_life(request.cookies.get('id'), 0)
                    
                    response = make_response(render_template('index.html', perso=True))
                    response.set_cookie('perso', str("1"))
                    return response
                
            if ('perso' in request.cookies and request.cookies.get('perso') == "1") or self.db_manager.getVite(request.cookies.get('id')) == 0:
                response = make_response(render_template('index.html', perso=True))
                response.set_cookie('perso', str("1"))
                return response

            
            food = FoodAPI()
            img_url, category = food.get_random_food()
            path_img = food.saveImage(img_url)
            actual_image = Image(path_img.split("static")[-1], category)
            #print(actual_image.path)
            
            images_all = self.getAllImages()
            categories = self.getCategories(actual_image,images_all)
            
            self.cibo_vincente = actual_image
            user = self.db_manager.get_user(request.cookies.get('id'))
            if user.timer in [0,-1]:
                time_attuale = int(time.time())
                self.db_manager.update_user_timer(user.id, time_attuale)
                user.timer = time_attuale
            return render_template('game.html', photo=actual_image, categorie=categories, user = user,secondi_totali=self.secondi_totali_timer)


        @self.app.route('/check_vittoria', methods=['GET', 'POST'])
        def check_vittoria():
            if request.method == 'POST':
                categoria_selected = request.form['radio_categorie']
                if categoria_selected == self.cibo_vincente.categoria:
                    self.db_manager.update_user_score(request.cookies.get('id'),50)
                    return render_template('vittoria.html', photo=self.cibo_vincente)
                else:
                    self.db_manager.update_user_score(request.cookies.get('id'),-25)
                    perso = self.db_manager.diminuisci_user_life(request.cookies.get('id'),-1)
                    if perso:
                        response = make_response(render_template('index.html', perso=True))
                        response.set_cookie('perso', str("1"))
                        return response
                    return render_template('sconfitta.html',photo=self.cibo_vincente)
            
        

        @self.app.route('/login', methods=['GET', 'POST'])
        def login():
            Login = True
            if 'username' in request.cookies:
                return render_template('index.html')
            if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']
                psw = hashlib.md5(password.encode()).hexdigest()
                id = self.db_manager.get_user_id(username, psw)
                if id is not None:
                    response = make_response(render_template('index.html'))
                    response.set_cookie('id', str(id))  # Imposta il cookie 'id' con il valore dell'id
                    response.set_cookie('username', str(username))
                    vite= self.db_manager.getVite(id)
                    if vite == 0:
                        response.set_cookie('perso', str("1"))
                    else:
                        response.set_cookie('perso', str("0"))
                    
                    
                    return response
                else:
                    Login = False
            return render_template('login.html', bool_login = Login)
        
        @self.app.route('/signin', methods=['GET', 'POST'])
        def signin():
            signin = True
            if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']
                name = request.form['name']
                email = request.form['email']
                
                
                psw = hashlib.md5(password.encode()).hexdigest()
                id = self.db_manager.register_user(name, username, psw, email)
                if id is not None:
                    return render_template('login.html',bool_login=True)
                else:
                    signin = False
            return render_template('signin.html', bool_signin = signin)
        
        @self.app.route('/classifica')
        def classifica():
            users = self.db_manager.get_all_users()
            users = self.ordinaUtenti(users)
            return render_template('classifica.html', users=users)
        
        @self.app.route('/logout')
        def logout():
            response = make_response(render_template('login.html',bool_login=True))
            response.set_cookie('id', '', expires=0)
            response.set_cookie('username', '', expires=0)
            response.set_cookie('perso', '', expires=0)
            return response
        
        @app.route('/window_closed', methods=['POST'])
        def window_closed():
            if request.content_type == 'text/plain':
                data = request.get_data(as_text=True)
                try:
                    json_data = json.loads(data)
                except ValueError:
                    return 'Invalid JSON', 400
            else:
                return 'Unsupported Media Type', 415
            
            # Gestisci i dati come JSON
            print('Finestra chiusa, dati:', json_data)
            response = make_response(render_template('index.html'))
            response.set_cookie('id', '', expires=0)
            response.set_cookie('username', '', expires=0)
            response.set_cookie('perso', '', expires=0)
            return response

    def getAllImages(self):
        images_all = []
        images_dir = os.path.join(self.app.static_folder, 'food_images')
        
        subdirectories = [name for name in os.listdir(images_dir) if os.path.isdir(os.path.join(images_dir, name))]
        
        
        for subdir in subdirectories:
            for filename in os.listdir(f"{images_dir}/{subdir}"):
                if filename.endswith('.jpg') or filename.endswith('.png'):
                    image_path = os.path.join(f"{images_dir}/{subdir}", filename)
                    image_path = image_path.split("static")[-1]
                    i = Image(image_path, subdir)
                    images_all.append(i)
                    
        return images_all
            
    def getCategories(self,actual_image,images_all):
        categories = set()  # Set per tenere traccia degli elementi visitati
        
        for i in images_all:
            if i not in categories :
                categories.add(i.categoria)
        
        categories = list(categories)
        random.shuffle(categories)
        cat_tagliato = categories[0:5]
        if actual_image.categoria in cat_tagliato:
            categories = categories[0:6]
        else:
            cat_tagliato.append(actual_image.categoria)
            categories = cat_tagliato
        random.shuffle(categories)
        return categories
    
    def ordinaUtenti(self,users):
        users.sort(key=lambda x: x.punteggio, reverse=True)
        return users