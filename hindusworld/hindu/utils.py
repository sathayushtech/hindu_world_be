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




# def image_path_to_binary(filename):
#     img_url = settings.FILE_URL
#     print("kkkkk",img_url)
#     img_path = os.path.join(img_url, filename) # Assuming settings.MEDIA_ROOT contains the directory where your images are stored
#     print(img_path, "---------------------------------")
#     if os.path.exists(img_path):
#         with open(img_path, "rb") as image_file:
#             image_data = image_file.read()
#             base64_encoded_image = base64.b64encode(image_data)
#             # print(base64_encoded_image)
#             return base64_encoded_image
#     else:
#         # print("File not found:", img_path)
#         return None


### to get the data even if the image is present or not present
# def image_path_to_binary(filename):
#     img_url = settings.FILE_URL
#     img_path = os.path.join(img_url, filename)  # Assuming settings.FILE_URL contains the directory where your images are stored

#     # Add debug logging to help identify the issue
#     print(f"Attempting to access image at path: {img_path}")
    
#     if os.path.exists(img_path):
#         try:
#             with open(img_path, "rb") as image_file:
#                 image_data = image_file.read()
#                 base64_encoded_image = base64.b64encode(image_data)
#                 return base64_encoded_image
#         except PermissionError as e:
#             print(f"Permission denied: {e}")
#             return None
#     else:
#         print(f"File not found: {img_path}")
#         return None


# def save_image_to_folder(image_location, _id, name,entity_type):
#     # Decode the base64 image data
#     image_data = base64.b64decode(image_location)
#     # Define the folder name using the _id
#     folder_name = str(_id)
#     # Get the base URL for the file storage
#     img_url = settings.FILE_URL
#     # Create the folder path
#     folder_path = os.path.join(img_url, entity_type, folder_name)
#     # Create the folder if it doesn't exist
#     if not os.path.exists(folder_path):
#         os.makedirs(folder_path)
#     # Define the image name
#     image_name = name + ".jpg"
#     # Define the full image path
#     image_path = os.path.join(folder_path, image_name)
#     # Save the image to the defined path
#     with open(image_path, "wb") as image_file:
#         image_file.write(image_data)
#     # Return the relative path to be stored in the database
#     relative_path = os.path.join(entity_type, folder_name, image_name)
#     return relative_path





def image_path_to_binary(filename):
    img_url = settings.FILE_URL
    def get_base64_encoded_image(img_path):
        if os.path.exists(img_path):
            with open(img_path, "rb") as image_file:
                image_data = image_file.read()
                base64_encoded_image = base64.b64encode(image_data)
                return base64_encoded_image
        else:
            return None
    if isinstance(filename, list):
        encoded_images = []
        for path in filename:
            img_path = os.path.join(img_url, path)
            base64_encoded_image = get_base64_encoded_image(img_path)
            if base64_encoded_image is not None:
                encoded_images.append(base64_encoded_image)
        return encoded_images
    else:
        img_path = os.path.join(img_url, filename)
        return get_base64_encoded_image(img_path)
    return None



def save_image_to_folder(image_data, _id, name, entity_type):
    decoded_image = base64.b64decode(image_data)
    folder_name = str(_id)
    img_url = settings.FILE_URL
    folder_path = os.path.join(img_url, entity_type, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    image_name = f"{name}_{uuid.uuid4().hex[:8]}.jpg"
    image_path = os.path.join(folder_path, image_name)
    with open(image_path, "wb") as image_file:
        image_file.write(decoded_image)
    relative_image_path = os.path.join(entity_type, folder_name, image_name)
    return relative_image_path











def save_video_to_folder(video_data, _id, name, entity_type):

    video_binary = base64.b64decode(video_data)
    folder_name = str(_id)
    folder_path = os.path.join(settings.FILE_URL, entity_type, folder_name)
    
    # Ensure the directory exists
    os.makedirs(folder_path, exist_ok=True)
    
    video_name = f"{name}_{uuid.uuid4().hex[:8]}.mp4"
    video_path = os.path.join(folder_path, video_name)
    
    with open(video_path, 'wb') as video_file:
        video_file.write(video_binary)
    
    relative_video_path = os.path.join(entity_type, folder_name, video_name)
    return relative_video_path

def video_path_to_binary(video_path):

    if not os.path.exists(video_path):
        return None
    
    with open(video_path, 'rb') as video_file:
        video_binary = base64.b64encode(video_file.read())
    
    return video_binary












def send_welcome_email(username):
    subject = 'Welcome to HinduWorld'
    html_content = f"""
    <html>
    <head>
        <title>Welcome to HinduWorld</title>
    </head>
    <body>
        <p>Dear {username},</p>
        <p>Namaste and Welcome to HinduWorld,</p>
        <p>We are thrilled to have you join our community. HinduWorld is dedicated to connecting Hindu organizations and fostering collaboration within our vibrant network.</p>
        <p>As a member, you can share information about your organization and activities. We look forward to your contributions and hope you will find the platform valuable.</p>
        <p>If you have any questions or need assistance, please do not hesitate to contact us at support@hinduworld.com.</p>
        <p>Best Regards,<br>
        HinduWorld Team</p>
    </body>
    </html>
    """
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [username]
    
    send_mail(
        subject=subject,
        message='',
        from_email=email_from,
        recipient_list=recipient_list,
        html_message=html_content
    )







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