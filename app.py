from flask import Flask, render_template, request, make_response
from food_api import FoodAPI
from image import Image
import os
import random
import hashlib

class PageManager:

    def __init__(self, app, db_manager):
        self.app = app
        self.db_manager = db_manager
        self.cibo_vincente = None

        @self.app.route('/')
        def index():
            if 'username' in request.cookies:
                return render_template('index.html')
            else:
                return render_template('login.html')

        @self.app.route('/game')
        def game():
            
            
            food = FoodAPI()
            img_url, category = food.get_random_food()
            path_img = food.saveImage(img_url)
            actual_image = Image(path_img.split("static")[-1], category)
            print(actual_image.path)
            
            images_all = []
            images_dir = os.path.join(app.static_folder, 'food_images')
            
            subdirectories = [name for name in os.listdir(images_dir) if os.path.isdir(os.path.join(images_dir, name))]
            
            categories = set()  # Set per tenere traccia degli elementi visitati
            
            for subdir in subdirectories:
                for filename in os.listdir(f"{images_dir}/{subdir}"):
                    if filename.endswith('.jpg') or filename.endswith('.png'):
                        image_path = os.path.join(f"{images_dir}/{subdir}", filename)
                        image_path = image_path.split("static")[-1]
                        i = Image(image_path, subdir)
                        images_all.append(i)
                        
                        # Verifica se l'elemento è già stato visitato
                        if i not in categories :
                            categories.add(i.categoria)
            
            categories = list(categories)
            random.shuffle(categories)
            categories = categories[0:5]
            categories.append(actual_image.categoria)
            random.shuffle(categories)
            
            self.cibo_vincente = actual_image
            return render_template('game.html', images=images_all, photo=actual_image, categorie=categories)


        @self.app.route('/check_vittoria', methods=['GET', 'POST'])
        def check_vittoria():
            
            
            if request.method == 'POST':
                categoria_selected = request.form['radio_categorie']
                if categoria_selected == self.cibo_vincente.categoria:
                    return render_template('vittoria.html', photo=self.cibo_vincente)
                else:
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
                    response.set_cookie('username', str(username))  # Imposta il cookie 'id' con il valore dell'id
                    
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
                    return render_template('login.html')
                else:
                    signin = False
            return render_template('signin.html', bool_signin = signin)
