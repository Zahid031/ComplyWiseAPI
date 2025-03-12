from django.db import models
from app.models import User
from app.modules.general_module.models.base_model import BaseModel
from django.utils import timezone

class OTP(BaseModel):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    otp_code=models.CharField(max_length=6)
    expires_at=models.DateTimeField()

    def is_valid(self):
        return self.expires_at > timezone.now()
    
    def __str__(self):
        return f"OTP for {self.user.email}: {self.otp_code}"
    
    


