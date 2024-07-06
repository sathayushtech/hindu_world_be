from django.db import models
from ..enums.user_status_enum import UserStatus
from ..enums import MemberStatus
import uuid
# import datetime
from django.utils import timezone
# from django.contrib.auth.models import AbstractUser
from ..utils import send_email,generate_otp,validate_email,send_sms
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser





class Register(AbstractUser):
    id = models.CharField(db_column='id', primary_key=True, max_length=45, default=uuid.uuid1, unique=True, editable=False) 
    full_name=models.CharField(db_column='full_name',max_length=200)
    name = models.CharField(max_length=200)
    dob = models.DateField()
    contact_number = models.CharField(db_column='contact_number',max_length=10,null=True,blank=True)
    father_name = models.CharField(db_column='father_name',max_length=200,null=True, blank=True)
    profile_pic = models.TextField(db_column='profile_pic', null=True, blank=True)
    is_member=models.CharField(max_length=50,choices=[(e.name,e.value) for e in MemberStatus],default=MemberStatus.FALSE.value)
    verification_otp = models.CharField(max_length=6, null=True, blank=True)
    verification_otp_created_time = models.DateTimeField(null=True)
    verification_otp_resend_count = models.IntegerField(default=0,db_column='verification_otp_resend_count')
    status = models.CharField(max_length=50,choices=[(e.name,e.value) for e in UserStatus],default=UserStatus.CREATED.value)
    forgot_password_otp = models.CharField(max_length=6, null=True, blank =True)
    forgot_password_otp_created_time = models.DateTimeField(null=True)
    forgot_password_otp_resend_count = models.IntegerField(default=0)
   
    
    class Meta:
        db_table = "profile"

    def __str__(self):

        return self.username
    


# @receiver(post_save, sender=Register)
# def send_email_or_sms_token(sender, instance, created, **kwargs):
#     if created:
#         try:
#             username = instance.username
#             if validate_email(username):
#                 otp = generate_otp()
#                 instance.verification_otp = otp
#                 instance.verification_otp_created_time = timezone.now()
#                 instance.save()
#                 send_email(username, otp)
#             else:
#                 otp = generate_otp()
#                 instance.verification_otp = otp
#                 instance.verification_otp_created_time = timezone.now()
#                 instance.save()
#                 send_sms(username, otp)
#         except Exception as e:
#             print(f"An error occurred while sending verification token: {e}")