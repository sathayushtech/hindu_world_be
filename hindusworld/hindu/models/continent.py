from django.db import models
import uuid

class continents(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False)
    name = models.CharField(db_column='name', max_length=45) 
    # capital = models.CharField(db_column='capital', max_length=45, blank=True, null=True) 
    alternativename = models.CharField(db_column='alternativename', max_length=45, blank=True, null=True) 
    desc = models.CharField(db_column='desc', max_length=250, blank=True, null=True) 
    type=models.CharField(db_column='type', max_length=30,choices=[('CONTINENT','CONTINENT')],default='CONTINENT')
    created_at = models.DateTimeField(db_column='created_at',auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        managed=False
        db_table = 'continent'
