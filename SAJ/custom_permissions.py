from django.contrib import admin
from django.contrib.auth.models import Group

class AdminPermissionMixin(admin.ModelAdmin):
    hidden_fields_group_map = {
        'مالک': {
            'student': [
                'is_superuser',
                'groups',
                'user_permissions',
                'branch',
                'grade',

            ],
  
            'teacher': [
                'is_superuser',
                'groups',
                'user_permissions',
                'password',
                'username',
                'branch',
                'date_joined',
            ],
            'manager': [
                'is_superuser',
                'groups',
                'user_permissions',
                'password',
                'username',
                'branch',
                'date_joined',
            ],
            'employee': [
                'is_superuser',
                'groups',
                'user_permissions',
                'password',
                'username',
                'branch',
                'date_joined',
            ],
        },


        'مدیر': {
            'student': [
                'is_superuser',
                'groups',
                'user_permissions',
                'branch',
                'grade',

            ],
  
            'teacher': [
                'is_superuser',
                'groups',
                'user_permissions',
                'password',
                'username',
                'branch',
                'date_joined',
            ],
            'manager': [
                'is_superuser',
                'groups',
                'user_permissions',
                'password',
                'username',
                'branch',
                'date_joined',
            ],
            'employee': [
                'is_superuser',
                'groups',
                'user_permissions',
                'password',
                'username',
                'branch',
                'date_joined',
            ],
        },
        

        'کارمند': {
            'student': [
                'is_superuser',
                'groups',
                'user_permissions',
                'branch',
                'grade',
                'is_staff',
                'is_active',

            ],
  
            'teacher': [
                'is_staff',
                'is_active',
                'is_superuser',
                'groups',
                'user_permissions',
                'password',
                'username',
                'branch',
                'date_joined',
            ],
            'manager': [
                'is_staff',
                'is_active',
                'is_superuser',
                'groups',
                'user_permissions',
                'password',
                'username',
                'branch',
                'date_joined',
            ],
            'employee': [
                'is_staff',
                'is_active',
                'is_superuser',
                'groups',
                'user_permissions',
                'password',
                'username',
                'branch',
                'date_joined',
            ],
        },

        'استاد': {
            'student': [
                'password',
                'is_superuser',
                'username',
                'is_staff',
                'is_active',
                'date_joined',
                'code_melli',
                'phone2',
                'phone',
                'email',
                'groups',
                'user_permissions',
            ],
        },

        
    }

    readonly_fields_group_map = {
        'استاد': {
            'student': ['phone'],
            'teacher': ['phone'],
        },

    }

    def get_model_name(self):
        """
        Return the name of the model in lowercase.
        This is useful for referencing model-specific configurations.
        """
        return self.model._meta.model_name

    def get_hidden_fields(self, request):
        """
        Returns the list of fields to hide based on the user's group and the current model.
        """
        model_name = self.get_model_name()

        for group_name, model_fields in self.hidden_fields_group_map.items():
            if request.user.groups.filter(name=group_name).exists():
                print (model_fields.get(model_name, []))
                return model_fields.get(model_name, [])
        return []

    def get_readonly_fields(self, request, obj=None):
        """
        Returns the list of fields to set as read-only based on the user's group and the current model.
        """
        model_name = self.get_model_name()

        for group_name, model_fields in self.readonly_fields_group_map.items():
            if request.user.groups.filter(name=group_name).exists():
                return model_fields.get(model_name, [])
        return super().get_readonly_fields(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        """
        Modify the form to hide fields based on the user's group and the current model.
        """
        form = super().get_form(request, obj, **kwargs)
        hidden_fields = self.get_hidden_fields(request)
        for field in hidden_fields:
            if field in form.base_fields:
                form.base_fields.pop(field)
        return form

    def get_queryset(self, request):
        """
        Filter the queryset based on the user's group and the current model.
        """
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='مالک').exists():
            # Apply custom queryset logic for group1
            return qs.filter(active=True)
        elif request.user.groups.filter(name='مدیر').exists():
            # Apply custom queryset logic for group2
            return qs.filter(active=False)

        elif request.user.groups.filter(name='کارمند').exists():
            # Apply custom queryset logic for group2
            return qs.filter(active=False)
        elif request.user.groups.filter(name='استاد').exists():
            # Apply custom queryset logic for group2
            return qs.filter(active=False)

        return qs
