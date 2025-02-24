from django.db import models

from authentication.models import CustomUser

class UserProfile(models.Model):
    user =models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name= models.CharField(max_length=20,blank=True,null=True)
    last_name=models.CharField(max_length=20,blank=True,null=True)
    phone_number=models.CharField(max_length=20,blank=True,null=True)
    address=models.TextField(blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.user.email


