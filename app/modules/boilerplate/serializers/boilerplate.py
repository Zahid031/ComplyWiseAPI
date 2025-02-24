from rest_framework import serializers
from ..models.boilerplate import Boilerplate

class BoilerplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boilerplate
        fields = ['id', 'username', 'email', 'password', 'created_at', 'updated_at']


#if you want to use HyperlinkedModelSerializer

# class ProfileSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ['url', 'user', 'bio']
#         extra_kwargs = {
#             'url': {'view_name': 'profile-detail', 'lookup_field': 'pk'},
#             'user': {'view_name': 'user-detail', 'lookup_field': 'pk'}
#         }

# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['url', 'name']
#         extra_kwargs = {
#             'url': {'view_name': 'group-detail', 'lookup_field': 'pk'}
#         }

# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     profile = serializers.HyperlinkedRelatedField(
#         view_name='profile-detail',
#         read_only=True
#     )
#     groups = serializers.HyperlinkedRelatedField(
#         many=True,
#         view_name='group-detail',
#         read_only=True
#     )

#     class Meta:
#         model = User
#         fields = ['url', 'id', 'username', 'email', 'profile', 'groups']
#         extra_kwargs = {
#             'url': {'view_name': 'user-detail', 'lookup_field': 'pk'}
#         }


# User JSON
# {
#     "url": "http://api.example.com/users/1/",
#     "id": 1,
#     "username": "johndoe",
#     "email": "johndoe@example.com",
#     "profile": "http://api.example.com/profiles/1/",
#     "groups": [
#         "http://api.example.com/groups/1/",
#         "http://api.example.com/groups/2/"
#     ]
# }

# Profile JSON
# {
#     "url": "http://api.example.com/profiles/1/",
#     "user": "http://api.example.com/users/1/",
#     "bio": "This is John Doe's bio."
# }

# Group JSON
# {
#     "url": "http://api.example.com/groups/1/",
#     "name": "Admins"
# }