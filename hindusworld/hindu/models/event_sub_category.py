from django.db import models
from .event_category import EventCategory
import uuid

class EventSubCategory(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False)
    name = models.CharField(db_column='name', max_length=45) 
    desc=models.CharField(db_column='desc',max_length=10000)
    category = models.ForeignKey(EventCategory,on_delete=models.SET_NULL,db_column='category', null=True, blank=True)
    image = models.CharField(db_column='image', max_length=250, blank=True, null=True)


    



    class Meta:
        managed=False
        db_table = 'event_subcategory'