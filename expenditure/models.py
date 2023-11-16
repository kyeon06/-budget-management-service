from django.db import models
from categories.models import Category

from common.models import BaseModel
from users.models import User

class Expenditure(BaseModel):
    money = models.PositiveIntegerField("지출금액")
    comment = models.TextField("지출메모", max_length=100, null=True, blank=True)
    is_sum = models.BooleanField("합계여부", default=True)
    expense_date = models.DateField("지출일")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


    class Meta:
        db_table = 'expenditure'


    def __str__(self):
        return f"{self.category}|{self.money}|{self.expense_date}"