import base64
import json


def save_base64_image(base64_string):
    image_data = base64.b64decode(base64_string)
    with open("output.png", "wb") as f:
        f.write(image_data)



with open("messages.json", "r") as json_data:
    
    data = json.load(json_data)
    img_path = data[0]['value']['image']
    
    
save_base64_image(img_path) 