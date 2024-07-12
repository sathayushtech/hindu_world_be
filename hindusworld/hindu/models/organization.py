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
    organization_name = models.CharField(max_length=200,)
    est_by = models.CharField(max_length=100)
    chairman = models.CharField(max_length=100)
    desc = models.TextField()
    est_date = models.CharField(max_length=50)
    reg_id = models.CharField(max_length=200)
    location = models.TextField()
    web_url = models.URLField()
    org_detail = models.CharField(max_length=200)
    mission = models.TextField()
    org_images = models.TextField()
    # org_images = models.JSONField(default=list, blank=True)
    # org_logo = models.JSONField(default=list, blank=True)
    org_logo = models.TextField(null=True,blank=True)
    status=models.CharField(max_length=50,choices=[(e.name,e.value) for e in status],default=status.PENDING.value)
    geo_site = models.CharField(max_length=50, choices=[(e.name, e.value) for e in GeoSite], default=GeoSite.DISTRICT.value)
    country=models.ForeignKey(Country,on_delete=models.CASCADE,related_name='country',db_column="country",null=True, blank=True)
    # organization_members = models.JSONField(null=True, blank=True)  
    object_id = models.ForeignKey('District', db_column='object_id', on_delete=models.SET_NULL, null=True, blank=True, related_name='organization')
    organization_members=models.CharField(max_length=10000)
    # content_type = models.ForeignKey(ContentType, db_column='content_type',on_delete=models.SET_NULL, null=True, blank=True)
    # root_map = GenericForeignKey('content_type', 'object_id')
    


  


    class Meta:
        managed=False
        db_table = "organization"
