from django.db import models

class Student(models.Model):
    student_id = models.AutoField(primary_key=True, max_length=10)
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    grade = models.CharField(max_length=2)
    branch = models.CharField(max_length=50)

    # string representation of the model
    def __str__(self):
        return f"{self.name} (ID: {self.student_id})"
