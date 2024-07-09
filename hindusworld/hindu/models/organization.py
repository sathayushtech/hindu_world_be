from django.db import models
import uuid
from django.core.validators import URLValidator, RegexValidator, MaxLengthValidator, MinLengthValidator
from django.core.exceptions import ValidationError
import re
from ..models import Country
from ..enums import status,GeoSite
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation


class Organization(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False)
    organization_name = models.CharField(
        max_length=200,
        validators=[
            MaxLengthValidator(200),
            MinLengthValidator(2, "Organization name cannot be empty")
        ]
    )
    est_by = models.CharField(
        max_length=100,
        validators=[
            MaxLengthValidator(500),
            MinLengthValidator(1, "Establisher name cannot be empty")
        ]
    )
    chairman = models.CharField(
        max_length=100,
        validators=[
            MaxLengthValidator(100),
            MinLengthValidator(1, "Chairman name cannot be empty")
        ]
    )
    desc = models.TextField(
        validators=[
            MinLengthValidator(1, "Description cannot be empty")
        ]
    )
    est_date = models.CharField(
        max_length=50,
        validators=[
            MaxLengthValidator(50),
            MinLengthValidator(1, "Establishment date cannot be empty"),
            RegexValidator(
             
                message="Date must be in YYYY-MM-DD format"
            )
        ]
    )
    reg_id = models.CharField(
        max_length=200,
        validators=[
            MaxLengthValidator(200),
            MinLengthValidator(1, "Registration ID cannot be empty")
        ]
    )
    location = models.TextField(
        validators=[
            MinLengthValidator(1, "Location cannot be empty")
        ]
    )
    web_url = models.URLField(
        validators=[ 
            URLValidator(message="Invalid URL format")
        ]
    )
    org_detail = models.CharField(
        max_length=200,
        validators=[
            MaxLengthValidator(200),
            MinLengthValidator(1, "Organization detail cannot be empty")
        ]
    )
    mission = models.TextField(
        validators=[
            MinLengthValidator(1, "Mission cannot be empty")
        ]
    )
    org_images = models.TextField(
        validators=[
            MinLengthValidator(1, "Organization images cannot be empty")
        ]
    )
    # org_images = models.JSONField(default=list, blank=True)
    # org_logo = models.JSONField(default=list, blank=True)
    org_logo = models.TextField(null=True,blank=True)
    status=models.CharField(max_length=50,choices=[(e.name,e.value) for e in status],default=status.PENDING.value)
    geo_site = models.CharField(max_length=50, choices=[(e.name, e.value) for e in GeoSite], default=GeoSite.VILLAGE.value)
    # country=models.ForeignKey(Country,on_delete=models.CASCADE,related_name='country',db_column="country")
    # organization_members = models.JSONField(null=True, blank=True)  
    object_id = models.ForeignKey('Village', db_column='object_id', on_delete=models.SET_NULL, null=True, blank=True, related_name='organization')
    organization_members=models.CharField(max_length=100000000000)
    # content_type = models.ForeignKey(ContentType, db_column='content_type',on_delete=models.SET_NULL, null=True, blank=True)
    # root_map = GenericForeignKey('content_type', 'object_id')
    


  


    class Meta:
        managed=False
        db_table = "organization"
