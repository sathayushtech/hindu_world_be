from django.db import models
import uuid



class Country(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False)
    name = models.CharField(db_column='name', max_length=45) 
    capital = models.CharField(db_column='capital', max_length=45, blank=True, null=True) 
    alternativename = models.CharField(db_column='alternativename', max_length=45, blank=True, null=True) 
    desc = models.CharField(db_column='desc', max_length=250, blank=True, null=True) 
    type=models.CharField(db_column='type', max_length=30, choices=[('COUNTRY','COUNTRY')],default='COUNTRY',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        managed=False
        db_table = 'country'




class organization(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False)
    organization_name = models.CharField(max_length=200)
    est_by = models.CharField(max_length=100)
    chairman = models.CharField(max_length=100,db_column='chairman')
    desc = models.TextField(db_column='desc',blank=True, null=True)
    est_date = models.CharField(max_length=200,blank=True, null=True)
    reg_id = models.CharField(max_length=200)
    location = models.TextField()
    wed_url = models.URLField()
    org_detail= models.CharField(max_length=200)
    mission = models.TextField()
    org_images= models.TextField()
    country=models.ForeignKey(Country,on_delete=models.CASCADE,blank=True, null=True,related_name='country')

    class Meta:
        db_table = 'organization'

