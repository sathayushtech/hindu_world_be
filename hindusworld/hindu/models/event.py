import uuid
from django.db import models
from ..models import Organization

class Events(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45, default=uuid.uuid1, unique=True, editable=False)
    name = models.CharField(db_column='name', max_length=45)
    start_date= models.CharField(max_length=20,null=True, blank=True)
    end_date= models.CharField(max_length=20,null=True, blank=True)
    brochure = models.TextField()
    location = models.CharField(max_length=100)
    organizer_name=models.CharField(max_length=100,null=True, blank=True)
    contact_details=models.CharField(max_length=100,null=True, blank=True)
    org_id = models.ForeignKey(Organization, db_column='org' ,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'event'
