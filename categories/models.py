from django.db import models

class Category(models.Model):
    name = models.CharField("카테고리명", max_length=50, unique=True)
    description = models.TextField("카테고리 설명", max_length=100)

    class Meta:
        db_table = "categories"
