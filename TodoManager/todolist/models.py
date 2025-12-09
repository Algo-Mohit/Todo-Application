from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE,default = None)
    task_name = models.CharField(max_length=60)
    is_completed = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.task_name,self.is_completed}"    


