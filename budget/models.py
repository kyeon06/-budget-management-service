from django.db import models
from categories.models import Category
from common.models import BaseModel
from users.models import User

class Budget(BaseModel):
    money = models.PositiveIntegerField("예산금액")
    start_date = models.DateField("시작일")
    end_date = models.DateField("종료일")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'budget'

    def __str__(self):
        return f"{self.user} : {self.category} : {self.money}"
