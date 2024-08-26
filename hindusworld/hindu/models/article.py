from django.db import models
import uuid
from ..models import SubCategory,Category
from django.utils.timesince import timesince
from django.utils import timezone
from ..enums.article_status_enum import ArticleStatus




class Article(models.Model):
    _id = models.CharField(db_column='_id',primary_key=True,max_length=45,default=uuid.uuid1,unique=True,editable=False)
    article = models.TextField()
    category_id = models.ForeignKey(Category,db_column='category_id',on_delete=models.CASCADE,max_length=45,null=True)
    subcategory_id = models.ForeignKey(SubCategory,db_column='sub_category',on_delete=models.CASCADE,max_length=45,null=True)
    status = models.CharField(db_column='status',max_length=45, choices=[(e.name, e.value) for e in ArticleStatus], default=ArticleStatus.PENDING.value)
    created_at = models.DateTimeField(auto_now_add=True)
    extracted_text = models.TextField(blank=True, null=True)

    @property
    def relative_time(self):
        return timesince(self.created_at, timezone.now())


    class Meta:
        db_table = "article"
        ordering = ['-created_at']