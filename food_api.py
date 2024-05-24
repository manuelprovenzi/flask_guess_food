import requests
from PIL import Image
from io import BytesIO
import os
class FoodAPI:
    def __init__(self):
        self.base_url = "https://foodish-api.com/api/"
        pass
    
    def get_random_food(self,category=None):
        url = self.base_url
        if category:
            url += f"images/{category}"
            self.cat = category
        response = requests.get(url)
        img_url = response.json()["image"]
        if not category:
            self.cat = self.getCaterogia(img_url)
        
        return img_url, self.cat

    def getCaterogia(self,img_url):
        return img_url.split("/")[-2]
    
    def saveImage(self,img_url):
        response = requests.get(img_url)
        img = Image.open(BytesIO(response.content))
        directory = f"static/food_images/{self.cat}"
        if not os.path.exists(directory):
            os.makedirs(directory)  # Crea la directory se non esiste

        image_path = os.path.join(directory, f"{img_url.split("/")[-1]}")
        img.save(image_path)
        return image_path
    
    