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

            Documents.objects.filter(parent_type='Employee', parent_id=instance.id).delete()


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





        
   
    # @action(detail=True, methods=['put'])

    # def update(self, request, *args, **kwargs):
        
    #     partial=kwargs.pop('partial',False)
    #     employee_data=request.data.copy()
    #     files=request.FILES.getlist('documents')
    #     employee=self.get_object()
    #     deleted_documents_ids=request.data.get('deleted_documents',[])
    #     serializer=self.get_serializer(employee,data=employee_data,partial=partial)

    #     if serializer.is_valid():
    #         employee=serializer.save()
    #         if deleted_documents_ids:
    #             Documents.objects.filter(id__in=deleted_documents_ids).delete()

    #         for file in files:
    #             documet=Documents.objects.create(
    #                 parent_type='Employee',
    #                 parent_id=employee.id,
    #                 file=file
    #             )
    #             employee.documents.add(documet)
    #         return Response(serializer.data,status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

