from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models.boilerplate import Boilerplate
from ..serializers.boilerplate import BoilerplateSerializer
from ..services.boilerplate import BoilerplateService

class BoilerplateViewSet(viewsets.ModelViewSet):
    queryset = Boilerplate.objects.all()
    serializer_class = BoilerplateSerializer
    user_service = BoilerplateService()

    #list: Handles GET /api/users/ to list all users.
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    #retrieve: Handles GET /api/users/{id}/ to get a single user by ID.
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    #create: Handles POST /api/users/ to create a new user.
    #if you want to use parent class and want to add some logic before and after
    def create(self, request, *args, **kwargs):
        # Custom logic before creating the user
        response = super().create(request, *args, **kwargs)
        # Custom logic after creating the user
        return response
    
    # #if you do no want to use parent class then you have to write everything here
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    #perform_create: Custom logic before saving a new user.
    def perform_create(self, serializer):
        # Call the service class method to handle custom logic before saving
        validated_data = self.user_service.create_user(serializer.validated_data)
        serializer.save(**validated_data)

    #update: Handles PUT /api/users/{id}/ to update a user completely.
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    #perform_update: Custom logic before updating a user.
    def perform_update(self, serializer):
        # Add custom logic before updating
        serializer.save()

    #partial_update: Handles PATCH /api/users/{id}/ to update a user partially.
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    #destroy: Handles DELETE /api/users/{id}/ to delete a user by ID.
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    #perform_destroy: Custom logic before deleting a user.
    def perform_destroy(self, instance):
        # Add custom logic before deleting
        instance.delete()