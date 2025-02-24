# from django.contrib.auth import get_user_model
# from oauth2_provider.models import AccessToken, Application
# from datetime import datetime, timedelta

# User = get_user_model()

# class AuthService:
#     @staticmethod
#     def create_access_token(user, application_name):
#         application = Application.objects.get(name=application_name)
#         expires = datetime.now() + timedelta(days=1)
#         access_token = AccessToken.objects.create(
#             user=user,
#             application=application,
#             expires=expires,
#             token=AccessToken.generate_token()
#         )
#         return access_token

#     @staticmethod
#     def get_user_by_token(token):
#         try:
#             access_token = AccessToken.objects.get(token=token)
#             return access_token.user
#         except AccessToken.DoesNotExist:
#             return None