# import uuid
# from django.db import models
# from .block import Block
# from .user import Register

# class Village(models.Model):
#     _id = models.CharField(db_column='_id', primary_key=True, max_length=45, default=uuid.uuid1, unique=True, editable=False)
#     name = models.CharField(db_column='name', max_length=45) 
#     desc = models.CharField(db_column='desc', max_length=500, blank=True, null=True, default=None)
#     pin_code = models.CharField(db_column='pin_code', max_length=15)
#     block = models.ForeignKey(Block, on_delete=models.CASCADE, related_name='villages') 
#     created_at = models.DateTimeField(auto_now_add=True)
#     image_location = models.CharField(max_length=500, null=True, blank=True)
#     user = models.ForeignKey(Register, on_delete=models.SET_NULL, related_name='villages', null=True)
#     type = models.CharField(db_column='type', max_length=30, choices=[('VILLAGE', 'VILLAGE'), ('AREA', 'AREA')], default='VILLAGE', blank=True)
#     old_village_code = models.CharField(db_column='old_village_code', max_length=45, null=True)

#     class Meta:
#         managed = True
#         db_table = 'village'






import uuid
from django.db import models
from ..models import *
# from .goshala import Goshala
from django.contrib.contenttypes.fields import GenericRelation
# from ..enums import EntityStatus
from .user import Register
# from .temple import Temple
from django.dispatch import receiver

from ..utils import *
from .block import Block

class Village(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False)
    name = models.CharField(db_column='name', max_length=45) 
    desc = models.CharField(db_column='desc', max_length=500, blank=True, null=True, default=None)
    # mapUrl = models.URLField(db_column='map_url', max_length=255, null=True, blank=True)  
    # status = models.CharField(db_column='status', max_length=50 ,choices=[(e.value, e.name) for e in EntityStatus], default=EntityStatus.INACTIVE.value)
    pin_code = models.CharField(db_column='pin_code', max_length=15)
    
    block = models.ForeignKey(Block, on_delete=models.CASCADE, related_name='villages') 
  
    created_at = models.DateTimeField(auto_now_add=True)
    
    image_location= models.CharField(max_length=500, null=True, blank=True)

    # user = models.ForeignKey(Register, on_delete=models.SET_NULL, related_name='villages',null=True)
    
    type=models.CharField(db_column='type', max_length=30, choices=[('VILLAGE','VILLAGE'),('AREA','AREA')],default='VILLAGE',blank=True)
    
    old_village_code = models.CharField(db_column='old_village_code', max_length=45, null=True)
    
    class Meta:
        managed = True
        db_table = 'village'

