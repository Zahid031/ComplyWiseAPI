from django.core.management.base import BaseCommand
from oauth2_provider.models import Application
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = "Create OAuth2 Application"

    def handle(self, *args, **kwargs):
        if not Application.objects.filter(client_type="confidential").exists():
            user = User.objects.filter(is_superuser=True).first()
            if not user:
                self.stdout.write(self.style.ERROR("No superuser found. Please create one first."))
                return

            app = Application.objects.create(
                name="API Client",
                user=user,
                client_type="confidential",
                authorization_grant_type="password"
            )
            self.stdout.write(self.style.SUCCESS(f"OAuth2 Application Created: {app.name}"))
        else:
            self.stdout.write(self.style.WARNING("OAuth2 Application already exists."))
