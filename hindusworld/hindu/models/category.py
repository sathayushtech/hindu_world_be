from django.db import models
import uuid

class Category(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False)
    name = models.CharField(db_column='name', max_length=45) 
    

    class Meta:
        managed=False
        db_table = 'category'