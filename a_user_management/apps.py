from django.apps import AppConfig


class AUserManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'a_user_management'
    verbose_name = 'کاربر ها'


    def ready(self):
        import a_user_management.signals  # Import the signals module