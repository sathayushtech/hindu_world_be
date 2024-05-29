from django.db import models
import uuid
from django.core.validators import URLValidator, RegexValidator, MaxLengthValidator, MinLengthValidator
from django.core.exceptions import ValidationError
import re
from ..models import Country


class organization(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False)
    organization_name = models.CharField(
        max_length=200,
        validators=[
            MaxLengthValidator(200),
            MinLengthValidator(2, "Organization name cannot be empty")
        ]
    )
    est_by = models.CharField(
        max_length=100,
        validators=[
            MaxLengthValidator(100),
            MinLengthValidator(1, "Establisher name cannot be empty")
        ]
    )
    chairman = models.CharField(
        max_length=100,
        validators=[
            MaxLengthValidator(100),
            MinLengthValidator(1, "Chairman name cannot be empty")
        ]
    )
    desc = models.TextField(
        validators=[
            MinLengthValidator(1, "Description cannot be empty")
        ]
    )
    est_date = models.CharField(
        max_length=50,
        validators=[
            MaxLengthValidator(50),
            MinLengthValidator(1, "Establishment date cannot be empty"),
            RegexValidator(
                regex=r'^\d{4}-\d{2}-\d{2}$',
                message="Date must be in YYYY-MM-DD format"
            )
        ]
    )
    reg_id = models.CharField(
        max_length=200,
        validators=[
            MaxLengthValidator(200),
            MinLengthValidator(1, "Registration ID cannot be empty")
        ]
    )
    location = models.TextField(
        validators=[
            MinLengthValidator(1, "Location cannot be empty")
        ]
    )
    web_url = models.URLField(
        validators=[
            URLValidator(message="Invalid URL format")
        ]
    )
    org_detail = models.CharField(
        max_length=200,
        validators=[
            MaxLengthValidator(200),
            MinLengthValidator(1, "Organization detail cannot be empty")
        ]
    )
    mission = models.TextField(
        validators=[
            MinLengthValidator(1, "Mission cannot be empty")
        ]
    )
    org_images = models.TextField(
        validators=[
            MinLengthValidator(1, "Organization images cannot be empty")
        ]
    )
    org_logo = models.TextField(
        validators=[
            MinLengthValidator(1, "Organization logo cannot be empty")
        ]
    )

    country=models.ForeignKey(Country,on_delete=models.CASCADE,related_name='country',db_column="country")
    # def clean(self):
    #     super().clean()
    #     if not re.match(r'^\d{4}-\d{2}-\d{2}$', self.est_date):
    #         raise ValidationError({'est_date': "Date must be in YYYY-MM-DD format"})

    #     # Add any other custom validations here

    # def save(self, *args, **kwargs):
    #     self.full_clean()  # This will call clean() and run all the validations
    #     super().save(*args, **kwargs)


    class Meta:
        db_table = "organization"
