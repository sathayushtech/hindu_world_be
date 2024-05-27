from django.core.mail import send_mail
import random
from django.conf import settings
import re
import string
import requests
import base64
import os



def image_path_to_binary(filename):
    img_url = settings.FILE_URL
    img_path = os.path.join(img_url, filename)  # Assuming settings.MEDIA_ROOT contains the directory where your images are stored
    # print(img_path, "---------------------------------")
    if os.path.exists(img_path):
        with open(img_path, "rb") as image_file:
            image_data = image_file.read()
            base64_encoded_image = base64.b64encode(image_data)
            # print(base64_encoded_image)
            return base64_encoded_image
    else:
        # print("File not found:", img_path)
        return None
    
def save_image_to_folder(org_images, _id,name):
    image_data = base64.b64decode(org_images)
    folder_name = str(_id)
    img_url = settings.FILE_URL

    folder_path = os.path.join(img_url,"organization", folder_name)
    print(folder_path,"11122223333")
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    image_name = name+".jpg"
    image_path = os.path.join(folder_path, image_name)
    with open(image_path, "wb") as image_file:
        image_file.write(image_data)
    return image_path