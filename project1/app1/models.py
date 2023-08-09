from django.db import models

# Create your models here.
class syllabus(models.Model):
    question=models.CharField(max_length=1000)
    answer=models.CharField(max_length=2000)
    def __str__(self):
        return self.question