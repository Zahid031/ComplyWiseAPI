from django.db import models
from app.modules.general_module.models.base_model import BaseModel
from app.modules.general_module.models.documents import Documents 
class Employee(BaseModel):
    GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other')
    )
    name=models.CharField(max_length=30)
    address=models.CharField(max_length=100)
    phone=models.CharField(max_length=15)
    email=models.EmailField(unique=True)
    gender=models.CharField(max_length=1, choices=GENDER_CHOICES)
    documents=models.ManyToManyField(Documents,related_name='employees',blank=True)

    def __str__(self):
        return self.name

   