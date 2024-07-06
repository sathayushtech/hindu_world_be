from django.core.mail import send_mail
import random
from django.conf import settings
import re
import string
import requests
import base64
import os
import uuid
from rest_framework.pagination import PageNumberPagination





class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100





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
    

    ############## single image##########
def save_image_to_folder(org_images, _id,name):
    image_data = base64.b64decode(org_images)
    folder_name = str(_id)
    img_url = settings.FILE_URL

    folder_path = os.path.join(img_url,"hinduworldimages", folder_name)
    print(folder_path,"11122223333")
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    image_name = name+".jpg"
    image_path = os.path.join(folder_path, image_name)
    with open(image_path, "wb") as image_file:
        image_file.write(image_data)
    return image_path



def save_logo_to_folder(org_images, _id,name):
    image_data = base64.b64decode(org_images)
    folder_name = str(_id)
    img_url = settings.FILE_URL

    folder_path = os.path.join(img_url,"hinduworldlogos", folder_name)
    print(folder_path,"11122223333")
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    image_name = name+".jpg"
    image_path = os.path.join(folder_path, image_name)
    with open(image_path, "wb") as image_file:
        image_file.write(image_data)
    return image_path


def save_profile_image_to_folder(org_images, _id,name):
    image_data = base64.b64decode(org_images)
    folder_name = str(_id)
    img_url = settings.FILE_URL

    folder_path = os.path.join(img_url,"profile_pic", folder_name)
    print(folder_path,"11122223333")
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    image_name = name+".jpg"
    image_path = os.path.join(folder_path, image_name)
    with open(image_path, "wb") as image_file:
        image_file.write(image_data)
    return image_path











def send_email(username, otp):
    subject = 'Your account verification email'
    message = f'Your OTP is: {otp}'
    print(message,"1111111111111")
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [username] 
    send_mail(subject, message, email_from, recipient_list)







# def send_email(emil,otp):
#     subject = f'your  account verfication email is:'
#     message = f'your otp is {otp}'
#     email_from = settings.EMAIL_HOST_USER
#     send_mail(subject,message,email_from,emil)


def generate_otp(length = 6):
    characters = string.digits
    otp = ''.join(random.choice(characters) for _ in range(length))
    return otp


def validate_email(email):
    email_regex = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$'
    if not re.match(email_regex, email):
        return False
    return True



sms_user = settings.SMS_USER
sms_password = settings.SMS_PASSWORD
sms_sender = settings.SMS_SENDER
sms_type = settings.SMS_TYPE
sms_template_id = settings.SMS_TEMPLATE_ID
RESEND_SMS = settings.RESEND_SMS_TEMP

def send_sms(username, otp):
    
    
    url = f"http://api.bulksmsgateway.in/sendmessage.php?user={sms_user}&password={sms_password}&mobile={username}&message=Dear user your OTP to verify your Gramadevata User account is {otp}. Thank You! team Sathayush.&sender={sms_sender}&type={sms_type}&template_id={sms_template_id}"

    print(url)  
    response = requests.get(url)
    print(response.text) 
    print("Sent Mobile OTP",username,otp,"ssssssssssssssssssssssssss")


def Resend_sms(username, otp):
    
    # url = f"http://api.bulksmsgateway.in/sendmessage.php?user={sms_user}&password={sms_password}&mobile={username}message=Dear user your OTP to reset your Gramadevata account Password is {otp}. Thank You! team Sathayush.&sender={sms_sender}&type={sms_type}&template_id={RESEND_SMS}"
    url = f"http://api.bulksmsgateway.in/sendmessage.php?user=Sathayushtech&password=Sathayushtech@1&mobile={username}&message=Dear user your OTP to reset your Gramadevata account Password is {otp}. Thank You! team Sathayush.&sender=STYUSH&type=3&template_id=1207170963828012432"

    print(url)  
    response = requests.get(url)
    print(response.text) 
    print("Sent Mobile OTP",username,otp,"rrrrrrrrrrrrrrrrrrrrr")