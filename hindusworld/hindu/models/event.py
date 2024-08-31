import uuid
from django.db import models
from ..models import Organization
from .event_category import EventCategory  
from ..enums import status,GeoSite,EventStatusEnum
from django.utils.timesince import timesince
from django.utils import timezone
from .district import District
from datetime import datetime
from .user import Register



class Events(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45, default=uuid.uuid1, unique=True, editable=False)
    name = models.CharField(db_column='name', max_length=45)
    start_date= models.DateField(db_column='start_date',max_length=20,null=True, blank=True)
    end_date= models.DateField(db_column='end_date',max_length=20,null=True, blank=True)
    start_time = models.TimeField(db_column='start_time',null=True,blank=True)
    end_time = models.TimeField(db_column = 'end_time',null=True,blank=True)
    brochure = models.TextField(db_column='brochure',null=True, blank=True)
    location = models.CharField(db_column='location',max_length=100)
    organizer_name=models.CharField(db_column='organizer_name',max_length=100,null=True, blank=True)
    contact_details=models.CharField(db_column='contact_details',max_length=100,null=True, blank=True)
    organization = models.ForeignKey(Organization, db_column='organization' ,on_delete=models.CASCADE)
    created_at = models.DateTimeField(db_column='created_at',auto_now_add=True)
    status=models.CharField(db_column='status',max_length=50,choices=[(e.name,e.value) for e in status],default=status.PENDING.value)
    event_images=models.JSONField(db_column='event_images',default=list,blank=True)
    live_stream_link=models.CharField(db_column='live_stream_link',max_length=100,null=True,blank=True)
    category = models.ForeignKey(EventCategory, db_column='category', on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.ForeignKey(District, db_column='object_id', on_delete=models.SET_NULL, null=True, blank=True, related_name='Events')
    geo_site = models.CharField(max_length=50, choices=[(e.name, e.value) for e in GeoSite], default=GeoSite.DISTRICT.value)
    event_status = models.CharField(db_column='event_status',max_length=50,choices=[(e.name, e.value) for e in EventStatusEnum],default=EventStatusEnum.UPCOMING.name)
    user = models.ForeignKey(Register, on_delete=models.SET_NULL, related_name='Events', null=True)


    @property
    def relative_time(self):
        if not self.start_date:
            return "Unknown"
        try:
            # Make the start_date timezone-aware
            start_date = timezone.make_aware(datetime.combine(self.start_date, datetime.min.time()))
        except Exception as e:
            return f"Invalid date: {e}"

        now = timezone.now().date()  # Get the current date

        if start_date.date() > now:
            diff = start_date.date() - now
            if diff.days == 1:
                return "1 day to go"
            else:
                return f"{diff.days} days to go"
        elif start_date.date() == now:
            return "Today"
        else:
            diff = now - start_date.date()
            if diff.days == 1:
                return "1 day ago"
            else:
                return f"{diff.days} days ago"
                

    def update_event_status(self):
        now = timezone.now()

        if self.end_date:
            try:
                # Use end_time if available; otherwise, use the end of the day (23:59:59)
                end_time = self.end_time if self.end_time else datetime.max.time()
                end_datetime = timezone.make_aware(datetime.combine(self.end_date, end_time))

                # Update event status based on whether the current time has passed the end time
                if end_datetime < now:
                    self.event_status = EventStatusEnum.COMPLETED.name
                else:
                    self.event_status = EventStatusEnum.UPCOMING.name

                # Save the updated event status to the database
                self.save()

            except Exception as e:
                print(f"Error updating event status: {e}")
                
    class Meta:
        db_table = 'event'