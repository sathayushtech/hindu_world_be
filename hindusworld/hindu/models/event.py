import uuid
from django.db import models
from ..models import Organization
from .event_sub_category import EventSubCategory
from .event_category import EventCategory  
from ..enums import status,GeoSite,EventStatusEnum
from django.utils.timesince import timesince
from django.utils import timezone
from .district import District
from datetime import datetime
from .user import Register
from dateutil.relativedelta import relativedelta
from pytz import timezone as pytz_timezone




class Events(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45, default=uuid.uuid1, unique=True, editable=False)
    name = models.CharField(db_column='name', max_length=45)
    start_date= models.DateTimeField(db_column='start_date',max_length=20,null=True, blank=True)
    end_date= models.DateTimeField(db_column='end_date',max_length=20,null=True, blank=True)
    # start_time = models.TimeField(db_column='start_time',null=True,blank=True)
    # end_time = models.TimeField(db_column = 'end_time',null=True,blank=True)
    brochure = models.TextField(db_column='brochure',null=True, blank=True)
    location = models.CharField(db_column='location',max_length=100)
    organizer_name=models.CharField(db_column='organizer_name',max_length=100,null=True, blank=True)
    contact_details=models.CharField(db_column='contact_details',max_length=100,null=True, blank=True)
    # organization = models.ForeignKey(Organization, db_column='organization' ,on_delete=models.CASCADE)
    created_at = models.DateTimeField(db_column='created_at',auto_now_add=True)
    status=models.CharField(db_column='status',max_length=50,choices=[(e.name,e.value) for e in status],default=status.PENDING.value)
    event_images=models.JSONField(db_column='event_images',default=list,blank=True,null=True)
    live_stream_link=models.CharField(db_column='live_stream_link',max_length=100,null=True,blank=True)
    category = models.ForeignKey(EventCategory, db_column='category', on_delete=models.CASCADE, null=True, blank=True)
    sub_category = models.ForeignKey(EventSubCategory, on_delete=models.SET_NULL, db_column='sub_category', null=True, blank=True)
    object_id = models.ForeignKey(District, db_column='object_id', on_delete=models.SET_NULL, null=True, blank=True, related_name='Events')
    geo_site = models.CharField(max_length=50, choices=[(e.name, e.value) for e in GeoSite], default=GeoSite.DISTRICT.value)
    event_status = models.CharField(db_column='event_status',max_length=50,choices=[(e.name, e.value) for e in EventStatusEnum],default=EventStatusEnum.UPCOMING.name)
    user = models.ForeignKey(Register, on_delete=models.SET_NULL, related_name='Events', null=True)
    event_details=models.CharField(max_length=1000,null=True,blank=True)




    @property
    def relative_time(self):
        if not self.start_date:
            return "Unknown"

        # Get IST timezone
        ist_timezone = pytz_timezone('Asia/Kolkata')

        # Get the current time in IST (timezone-aware)
        now = timezone.now().astimezone(ist_timezone)

        # Convert start_date to a timezone-aware datetime in IST
        start_datetime = self.start_date
        if timezone.is_naive(start_datetime):
            # If start_date is naive, localize it to IST timezone
            start_datetime = ist_timezone.localize(start_datetime)
        else:
            # If already timezone-aware, convert to IST
            start_datetime = start_datetime.astimezone(ist_timezone)

        # Check if the event has already started or not
        if start_datetime > now:
            diff = relativedelta(start_datetime, now)
            if diff.years > 0:
                return f"{diff.years} year{'s' if diff.years > 1 else ''} to go"
            elif diff.months > 0:
                return f"{diff.months} month{'s' if diff.months > 1 else ''} to go"
            elif diff.days > 0:
                return f"{diff.days} day{'s' if diff.days > 1 else ''} to go"
            elif diff.hours > 0:
                return f"{diff.hours} hour{'s' if diff.hours > 1 else ''} to go"
            elif diff.minutes > 0:
                return f"{diff.minutes} minute{'s' if diff.minutes > 1 else ''} to go"
            else:
                return "Less than a minute to go"
        else:
            # Event has already started, so show the time since it started
            diff = relativedelta(now, start_datetime)
            if diff.years > 0:
                return f"{diff.years} year{'s' if diff.years > 1 else ''} ago"
            elif diff.months > 0:
                return f"{diff.months} month{'s' if diff.months > 1 else ''} ago"
            elif diff.days > 0:
                return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
            elif diff.hours > 0:
                return f"{diff.hours} hour{'s' if diff.hours > 1 else ''} ago"
            elif diff.minutes > 0:
                return f"{diff.minutes} minute{'s' if diff.minutes > 1 else ''} ago"
            else:
                return "Less than a minute ago"


    def update_event_status(self):
        now = timezone.now()

        if self.end_date:
            # Check if end_date is naive, if so, make it timezone-aware
            if timezone.is_naive(self.end_date):
                end_datetime = timezone.make_aware(self.end_date.replace(hour=23, minute=59, second=59))
            else:
                end_datetime = self.end_date.replace(hour=23, minute=59, second=59)

            if end_datetime < now and self.event_status != EventStatusEnum.COMPLETED.name:
                self.event_status = EventStatusEnum.COMPLETED.name
                self.save(update_fields=['event_status'])

        elif self.start_date:
            # Check if start_date is naive, if so, make it timezone-aware
            if timezone.is_naive(self.start_date):
                start_datetime = timezone.make_aware(self.start_date.replace(hour=0, minute=0, second=0))
            else:
                start_datetime = self.start_date.replace(hour=0, minute=0, second=0)

            if start_datetime < now and self.event_status != EventStatusEnum.COMPLETED.name:
                self.event_status = EventStatusEnum.COMPLETED.name
                self.save(update_fields=['event_status'])


    def save(self, *args, **kwargs):
    # Update event status before saving
        self.update_event_status()
        super(Events, self).save(*args, **kwargs)


                
    class Meta:
        db_table = 'event'