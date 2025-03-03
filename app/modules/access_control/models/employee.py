from django.db import models

#from django.contrib.auth.models import User
class Employee(models.Model):
    GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other')
    )
    #user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='employee')
    name=models.CharField(max_length=30)
    address=models.CharField(max_length=50)
    phone=models.CharField(max_length=15)
    email=models.EmailField(unique=True)
    gender=models.CharField(max_length=1, choices=GENDER_CHOICES)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
   