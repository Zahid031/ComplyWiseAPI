from rest_framework import serializers
from ..models.documents import Documents
from app.modules.access_control.models.employee import Employee
from django.db import models



class DocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Documents
        fields='__all__'



        # extra_kwargs={
        #     'employee':{'write_only':True}
        # }
        # def create(self,validated_data):
        #     employee_id=validated_data.pop('employee')
        #     employee=Employee.objects.get(id=employee_id)
        #     document=Documents.objects.create(employee=employee, **validated_data)
        #     return document
        