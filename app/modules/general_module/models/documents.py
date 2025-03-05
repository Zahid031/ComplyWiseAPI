from .base_model import BaseModel

from django.db import models
class Documents(BaseModel):
    parent_type=models.CharField(max_length=100,null=True, blank=True)
    parent_id=models.IntegerField(null=True, blank=True)
    file=models.FileField(upload_to='documents/')
    def __str__(self):
        return f"Documents for {self.file.name}"
    
    
