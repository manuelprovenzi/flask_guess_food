from flask import Flask, render_template
from food_api import FoodAPI

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game')
def game():
    food = FoodAPI()
    img_url,category = food.get_random_food()
    food.saveImage(img_url)
    return render_template('game.html')