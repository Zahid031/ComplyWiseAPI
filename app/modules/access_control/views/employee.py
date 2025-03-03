from django.shortcuts import render

from rest_framework import viewsets
from ..models.employee import Employee
from ..serializers.employee import EmployeeSerializer
import random
import string
from django.contrib.auth.models import User

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializer

