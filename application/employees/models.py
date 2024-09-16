from django.db import models

class Employee(models.Model):
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    date_of_birth = models.DateField()

    def __str__(self):
        return self.full_name
