from django.contrib.auth import get_user_model
from oauth2_provider.models import AccessToken, Application
from datetime import datetime, timedelta

User = get_user_model()

class AuthService:
    @staticmethod
    def create_access_token(user, application_name="ComplyWiseAPI"):
        try:
            application = Application.objects.get(name=application_name)
        except Application.DoesNotExist:
            application = Application.objects.create(
                name=application_name,
                client_type=Application.CLIENT_CONFIDENTIAL,  
                authorization_grant_type=Application.GRANT_PASSWORD,  
                user=None  
            )
            print(f"Created OAuth2 Application: {application_name}")

        expires = datetime.now() + timedelta(days=1)
        access_token = AccessToken.objects.create(
            user=user,
            application=application,
            expires=expires,
            token=AccessToken.generate_new_token()
        )
        return access_token

    @staticmethod
    def get_user_by_token(token):
        try:
            access_token = AccessToken.objects.get(token=token)
            if access_token.is_expired():
                return None
            return access_token.user
        except AccessToken.DoesNotExist:
            return None