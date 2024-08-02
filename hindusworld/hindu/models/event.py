import uuid
from django.db import models
from ..models import Organization
from ..enums import status
from django.utils.timesince import timesince
from django.utils import timezone

class Events(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45, default=uuid.uuid1, unique=True, editable=False)
    name = models.CharField(db_column='name', max_length=45)
    start_date= models.CharField(db_column='start_date',max_length=20,null=True, blank=True)
    end_date= models.CharField(db_column='end_date',max_length=20,null=True, blank=True)
    brochure = models.TextField(db_column='brochure',null=True, blank=True)
    location = models.CharField(db_column='location',max_length=100)
    organizer_name=models.CharField(db_column='organizer_name',max_length=100,null=True, blank=True)
    contact_details=models.CharField(db_column='contact_details',max_length=100,null=True, blank=True)
    organization = models.ForeignKey(Organization, db_column='organization' ,on_delete=models.CASCADE)
    created_at = models.DateTimeField(db_column='created_at',auto_now_add=True)
    status=models.CharField(db_column='status',max_length=50,choices=[(e.name,e.value) for e in status],default=status.PENDING.value)
    event_images=models.JSONField(db_column='event_images',default=list,blank=True)
    live_stream_link=models.CharField(db_column='live_stream_link',max_length=100,null=True,blank=True)


    @property
    def relative_time(self):
        return timesince(self.created_at, timezone.now())

    class Meta:
        db_table = 'event'
