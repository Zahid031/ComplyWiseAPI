from app.modules.general_module.models.base_model import BaseModel
from django.db import models
from django.utils.text import slugify
class Menu(BaseModel):
    title=models.CharField(max_length=100)
    name=models.CharField(max_length=100,unique=True)
    url=models.CharField(max_length=100,blank=True,null=True)

    def save(self, *args, **kwargs):
        if not self.url:
            self.url = f"/{slugify(self.name)}/"
            super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    



    