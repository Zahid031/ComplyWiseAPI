from django.shortcuts import render
from rest_framework.response import Response
from django.db import transaction
from rest_framework.decorators import action
from ...general_module.models.documents import Documents
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from app.modules.access_control.models.employee import Employee
from app.modules.general_module.models.documents import Documents
from app.modules.access_control.serializers.employee import EmployeeSerializer
from app.modules.general_module.serializers.documents import DocumentsSerializer
import json
import hashlib
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

def get_file_hash(file):
    hasher = hashlib.sha256()
    for chunk in file.chunks():
        hasher.update(chunk)
    return hasher.hexdigest()


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    parser_classes = (MultiPartParser, FormParser)  
    http_method_names=['get', 'post','put', 'patch', 'delete']


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
    


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            serializer.save()

            files_to_delete = request.data.get('files_to_delete', [])
            try:
                files_to_delete = json.loads(files_to_delete)  
            except json.JSONDecodeError:
                return Response(
                    {"error": "Invalid format for 'files_to_delete'. Expected a JSON array."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if files_to_delete:
                to_delete=Documents.objects.filter(parent_type='Employee',parent_id=instance.id)
                for doc in to_delete:
                    if doc.file:
                        file_path = doc.file.path
                        if default_storage.exists(file_path):
                            default_storage.delete(file_path)
                to_delete.delete()           

            files = request.FILES.getlist('documents')
            if files:
                for file in files:
                    document = Documents.objects.create(
                        parent_type='Employee',
                        parent_id=instance.id,
                        file=file
                    )
                    instance.documents.add(document)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)












    # def partial_update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     employee_data = request.data.copy()
    #     files = request.FILES.getlist('documents')
    #     #document_ids_to_delete = request.data.getlist('document_ids_to_delete', [])  
    #     # for doc_id in document_ids_to_delete:
    #     #     document = Documents.objects.filter(id=doc_id, parent_id=instance.id, parent_type="Employee").first()
    #     #     if document:
    #     #         document.delete()

    #     serializer = self.get_serializer(instance, data=employee_data, partial=True)
    #     if serializer.is_valid():
    #         employee = serializer.save()

    #         for file in files:
    #             document = Documents.objects.create(
    #                 parent_type='Employee',
    #                 parent_id=employee.id,
    #                 file=file
    #             )
    #             employee.documents.add(document)

    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





        
