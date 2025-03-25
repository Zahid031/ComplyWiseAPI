from ...general_module.models.base_model import BaseModel
from django.db import models
from app.models import User
from .menu import Menu

class Role(BaseModel):
    name=models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name
    
class RolePermission(BaseModel):
    role=models.ForeignKey(Role, on_delete=models.RESTRICT,related_name="permissions")#cascade change
    menu=models.ForeignKey(Menu, on_delete=models.RESTRICT)
    can_create=models.BooleanField(default=False)
    can_read=models.BooleanField(default=False)
    can_update=models.BooleanField(default=False)
    can_delete=models.BooleanField(default=False)
    can_reports=models.BooleanField(default=False)
    list_view=models.BooleanField(default=False)

    class Meta:
        unique_together = ('role', 'menu')

    def __str__(self):
        return self.role.name+"-"+self.menu.name

class UserRole(BaseModel):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    role=models.ForeignKey(Role,on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'role')

        def __str__(self):
            return self.user.email+"-"+self.role.name
        

    