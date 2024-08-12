import uuid
from django.db import models
from ..models import Organization
from ..enums import status,TrainingType
  





class Training(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45, default=uuid.uuid1, unique=True, editable=False)
    name = models.CharField(db_column='name', max_length=45)
    desc=models.CharField(db_column='desc',max_length=1000000)
    image=models.TextField()
    location=models.CharField(db_column='location',max_length=100)
    duration=models.CharField(db_column='duration',max_length=100)
    time=models.CharField(db_column='time',max_length=100)
    trainer_name=models.CharField(db_column='trainer_name',max_length=100)
    contact_details=models.CharField(db_column='contact_details',max_length=100)
    created_at = models.DateTimeField(db_column='created_at',auto_now_add=True)
    status=models.CharField(db_column='status',max_length=50,choices=[(e.name,e.value) for e in status],default=status.PENDING.value)
    video=models.TextField(db_column='video')
    training_type = models.CharField(db_column='training_type', max_length=7, choices=[(e.value, e.value) for e in TrainingType])  # Add this line







    
    class Meta:
        db_table = 'training'
