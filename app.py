from flask import Flask, render_template
from food_api import FoodAPI
from image import Image
import os


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game')
def game():
    food = FoodAPI()
    img_url, category = food.get_random_food()
    path_img = food.saveImage(img_url)
    actual_image = Image(path_img, category)
    
    images_all = []
    images_dir = os.path.join(app.static_folder, 'food_images')
    
    subdirectories = [name for name in os.listdir(images_dir) if os.path.isdir(os.path.join(images_dir, name))]
    
    for subdir in subdirectories:
        for filename in os.listdir(f"{images_dir}/{subdir}"):
            if filename.endswith('.jpg') or filename.endswith('.png'):
                image_path = os.path.join(f"{images_dir}/{subdir}", filename)
                i = Image(image_path, subdir)
                images_all.append(i)
    
    return render_template('game.html', images=images_all, photo=actual_image)

