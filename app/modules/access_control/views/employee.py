from django.shortcuts import render
from rest_framework.response import Response
from ...general_module.models.documents import Documents
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from app.modules.access_control.models.employee import Employee
from app.modules.general_module.models.documents import Documents
from app.modules.access_control.serializers.employee import EmployeeSerializer
from app.modules.general_module.serializers.documents import DocumentsSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    parser_classes = (MultiPartParser, FormParser)  


    def create(self, request, *args, **kwargs):
        employee_data = request.data.copy()  
        files = request.FILES.getlist('documents')  
        serializer = self.get_serializer(data=employee_data)

        if serializer.is_valid():
            employee = serializer.save()  
            for file in files:
                document=Documents.objects.create(
                    parent_type='Employee',
                    parent_id=employee.id,
                    file=file
                    )
                employee.documents.add(document)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

