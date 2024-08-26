from django.db import models
import uuid


class ArticleCategory(models.Model):
    _id = models.CharField(db_column='_id',primary_key=True,default=uuid.uuid1,editable=False,max_length=45,unique=True,)
    name = models.CharField(db_column='name',max_length=100)
    desc = models.TextField(db_column='desc',null=True)
    # image = models.TextField(db_column='image',null=True,blank=True)



    class Meta:
        managed = False
        db_table = 'article_category'