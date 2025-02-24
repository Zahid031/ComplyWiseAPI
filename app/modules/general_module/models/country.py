from django.db import models
from .base_model import BaseModel

class Country(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    iso_alpha3_code = models.CharField(max_length=3, unique=True)
    iso_alpha2_code = models.CharField(max_length=2, unique=True)
    
    def __str__(self):
        return self.name