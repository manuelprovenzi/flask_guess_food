from flask import Flask, render_template, request
from food_api import FoodAPI
from image import Image
import os
import random


app = Flask(__name__)

cibo_vincente = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game')
def game():
    global cibo_vincente
    
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
    
    cibo_vincente = actual_image
    return render_template('game.html', images=images_all, photo=actual_image, categorie=categories)


@app.route('/check_vittoria', methods=['GET', 'POST'])
def check_vittoria():
    global cibo_vincente
    
    if request.method == 'POST':
        categoria_selected = request.form['radio_categorie']
        if categoria_selected == cibo_vincente.categoria:
            return render_template('vittoria.html', photo=cibo_vincente)
        else:
            return render_template('sconfitta.html',photo=cibo_vincente)
    