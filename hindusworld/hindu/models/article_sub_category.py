from django.db import models
from ..models import ArticleCategory
import uuid


class ArticleSubCategory(models.Model):
    _id = models.CharField(db_column='_id',primary_key=True,default=uuid.uuid1,editable=False,max_length=45,unique=True,)
    name = models.CharField(db_column='name',max_length=100)
    desc = models.CharField(db_column='desc',max_length=5000)
    # image = models.TextField(db_column='image',null=True,blank=True)
    category_id = models.ForeignKey(ArticleCategory,db_column='category_id',on_delete=models.SET_NULL,null=True)



    class Meta:
        managed = False
        db_table = 'article_sub_category'
    