from django.db import models
from app.modules.general_module.models.base_model import BaseModel
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Custom user manager
class EVUserManager(BaseUserManager):
    def create_user(self, email, name, mobile_no, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, mobile_no=mobile_no)
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, mobile_no, password=None):
        user = self.create_user(email, name, mobile_no, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class EVUser(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    mobile_no = models.CharField(max_length=20)
    password = models.CharField(max_length=255)  # Stored as a hashed password
    email_verified_at = models.DateTimeField(null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Required for admin access

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='ev_users',  # Add related_name to avoid clashes
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='ev_users',  # Add related_name to avoid clashes
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    objects = EVUserManager()  # Link custom manager

    USERNAME_FIELD = "email"  # Use email instead of username for authentication
    REQUIRED_FIELDS = ["name", "mobile_no"]  # Required fields for superuser creation

    def __str__(self):
        return self.name