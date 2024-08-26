import uuid
from django.db import models
from ..models import Organization
from .event_category import EventCategory  
from ..enums import status,GeoSite,EventStatusEnum
from django.utils.timesince import timesince
from django.utils import timezone
from .district import District
from datetime import datetime


class Events(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45, default=uuid.uuid1, unique=True, editable=False)
    name = models.CharField(db_column='name', max_length=45)
    start_date= models.CharField(db_column='start_date',max_length=20,null=True, blank=True)
    end_date= models.CharField(db_column='end_date',max_length=20,null=True, blank=True)
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
    



    @property
    def relative_time(self):
        if not self.start_date or not self.start_time:
            return "Unknown"

        try:
            # Convert strings to datetime
            start_date = datetime.strptime(self.start_date, '%d-%m-%Y').date()
            # Remove microseconds from the time string
            start_time_str = self.start_time.split('.')[0]
            start_time = datetime.strptime(start_time_str, '%H:%M:%S').time()
            start_datetime = timezone.make_aware(datetime.combine(start_date, start_time))
        except ValueError as e:
            return f"Invalid date or time format: {e}"

        now = timezone.now()

        # Compute relative time
        if start_datetime > now:
            diff = start_datetime - now
            if diff.days == 0:
                hours, remainder = divmod(diff.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                return f"{hours} hours, {minutes} minutes to go"
            elif diff.days == 1:
                return "1 day to go"
            else:
                return f"{diff.days} days to go"
        else:
            diff = now - start_datetime
            if diff.days == 0:
                hours, remainder = divmod(diff.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                return f"{hours} hours, {minutes} minutes ago"
            elif diff.days == 1:
                return "1 day ago"
            else:
                return f"{diff.days} days ago"
    def update_event_status(self):
        now = timezone.now()
        if self.end_date and self.end_time:
            end_datetime_str = f"{self.end_date} {self.end_time.split('.')[0]}"
            try:
                end_datetime = datetime.strptime(end_datetime_str, '%d-%m-%Y %H:%M:%S')
                end_datetime = timezone.make_aware(end_datetime)
                
                if end_datetime < now:
                    self.event_status = EventStatusEnum.COMPLETED.name
                else:
                    self.event_status = EventStatusEnum.UPCOMING.name
                self.save()
            except ValueError as e:
                print(f"Error updating event status: {e}")

    class Meta:
        db_table = 'event'
