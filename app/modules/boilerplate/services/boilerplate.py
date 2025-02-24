from ..models.boilerplate import Boilerplate

class BoilerplateService:
    def create_user(self, data):
        # Add custom logic before saving
        # Perform extra calculations and validations here
        # Example: data['full_name'] = f"{data['first_name']} {data['last_name']}"
        return data

    def update_user(self, instance, data):
        # Add custom logic before updating
        # Perform extra calculations and validations here
        # Example: data['full_name'] = f"{data['first_name']} {data['last_name']}"
        return data

    def delete_user(self, instance):
        # Add custom logic before deleting
        pass

    def get_users(self):
        # Add custom logic before retrieving data
        return Boilerplate.objects.all()