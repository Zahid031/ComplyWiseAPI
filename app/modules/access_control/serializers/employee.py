from rest_framework import serializers
from django.contrib.auth.models import User
from ..models.employee import Employee
import random
import string

class EmployeeSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Employee
        fields = ['id', 'name', 'address','phone','email', 'gender']




    
    # def create(self, validated_data):
    #     if 'password' not in validated_data:
    #         password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    #     else:
    #         password = validated_data.pop('password')
        
    #     email = validated_data.get('email')
    #     name = validated_data.get('name')
    #     username = email.split('@')[0]
    #     # user = User.objects.create_user(
    #     #     username=username,
    #     #     email=email,
    #     #     password=password,
    #     #     first_name=name.split()[0] if ' ' in name else name,
    #     #     last_name=name.split()[-1] if ' ' in name else ''
    #     # )
        
    #     employee = Employee.objects.create(user=user, **validated_data)
        
    #     from django.core.mail import send_mail
        
    #     subject = 'Your Employee Account has been created'
    #     message = f'''
    #     Hello {name},
        
    #     Your employee account has been created successfully.
        
    #     Your login details:
    #     Username: {username}
    #     Password: {password}
        
    #     Please change your password after the first login.

    #     '''
        
    #     send_mail(
    #         subject,
    #         message,
    #         '1902045zahid@gmail.com', 
    #         [email],
    #         fail_silently=False,
    #     )
        
    #     return employee