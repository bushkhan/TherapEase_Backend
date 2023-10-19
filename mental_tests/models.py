from django.db import models
from django.db import models
from accounts.models import CustomUser



# Create your models here.
class AnxietyTest(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    question_1 = models.IntegerField()
    question_2 = models.IntegerField()
    question_3 = models.IntegerField()
    question_4 = models.IntegerField()
    question_5 = models.IntegerField()
    question_6 = models.IntegerField()
    question_7 = models.IntegerField()
    total = models.IntegerField()
    result = models.CharField(max_length=255)
    
    def user_email(self):
        return self.user_id.email

    def __str__(self):
        return f"AnxietyTest for {self.user_email()}"