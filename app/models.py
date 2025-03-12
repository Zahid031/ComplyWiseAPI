from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from app.modules.general_module.models.base_model import BaseModel

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True) 
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
    
    
class User(AbstractUser, BaseModel):
    username = None  
    email = models.EmailField(unique=True)
    full_name=models.CharField(max_length=100,null=False, blank=True)
    mobile_no=models.CharField(max_length=15, null=False, blank=True)
    password=models.CharField(max_length=100,null=True, blank=True)
    #email_verified=models.BooleanField(default=False)
    email_verified_at=models.DateTimeField(null=True, blank=True)
    
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name','mobile_no']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
