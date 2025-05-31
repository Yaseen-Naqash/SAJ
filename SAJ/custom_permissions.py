from django.contrib import admin
from django.contrib.auth.models import Group
from a_course_management.models import SectionStudent, HomeWork, HomeWorkDocument, Attendance, Section, Course, SectionTimeSlot, Exam
from a_financial_management.models import Receipt
from a_notification_management.models import Notification, News
from a_survey_management.models import Survey, Question, Answer, Choice
from a_user_management.models import Student, Manager, Employee

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
            'sectionstudent': [
                'section',
                'student',
                'activity',
                'exam_score',
                'start_date',
                'end_date',
                'score',
                ],
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

        qs = super().get_queryset(request)

        user = request.user
        branch_filter = request.session.get('branch', None)
        # print('test')



        if branch_filter:
            # Apply branch-based filtering
            if self.model == Course:
                qs = qs.filter(branch__id=branch_filter)

            elif self.model == Section:
                qs = qs.filter(course__branch__id=branch_filter)

            elif self.model == SectionStudent:
                qs = qs.filter(section__course__branch__id=branch_filter)

            elif self.model == SectionTimeSlot:
                qs = qs.filter(section__course__branch__id=branch_filter)

            elif self.model == Attendance:
                qs = qs.filter(section__course__branch__id=branch_filter)

            elif self.model == Exam:
                qs = qs.filter(section__course__branch__id=branch_filter)

            elif self.model == HomeWork:
                qs = qs.filter(section__course__branch__id=branch_filter)

            elif self.model == HomeWorkDocument:
                qs = qs.filter(homeWork__section__course__branch__id=branch_filter)

            elif self.model == Receipt:
                qs = qs.filter(branch__id=branch_filter)

            elif self.model == Notification:
                qs = qs.filter(branch__id=branch_filter)

            elif self.model == Notification:
                qs = qs.filter(branch__id=branch_filter)

            elif self.model == Survey:
                qs = qs.filter(branch__id=branch_filter)

            elif self.model == Question:
                qs = qs.filter(survey__branch__id=branch_filter)

            elif self.model == Choice:
                qs = qs.filter(question__survey__branch__id=branch_filter)

            elif self.model == Answer:
                qs = qs.filter(question__survey__branch__id=branch_filter)

            elif self.model == Student:
                qs = qs.filter(branch__id=branch_filter)

            elif self.model == Manager:
                qs = qs.filter(branch__id=branch_filter)
                
            elif self.model == Employee:
                qs = qs.filter(branch__id=branch_filter)

        """
        Filter the queryset based on the user's group and the current model.
        """
        if request.user.groups.filter(name='مالک').exists():
            # Apply custom queryset logic for group1
            return qs
        elif request.user.groups.filter(name='مدیر').exists():
            # Apply custom queryset logic for group2
            return qs

        elif request.user.groups.filter(name='کارمند').exists():
            # Apply custom queryset logic for group2
            return qs
        elif request.user.groups.filter(name='استاد').exists():

            if self.model == SectionStudent:
                # Filter the queryset for the logged-in teacher
                return qs.filter(section__teacher=request.user)
            
            if self.model == HomeWork:
                # Filter the queryset for the logged-in teacher
                return qs.filter(teacher=request.user)
            
            if self.model == HomeWorkDocument:
                # Filter the queryset for the logged-in teacher
                return qs.filter(homeWork__teacher=request.user)
            
            if self.model == Attendance:
                # Filter the queryset for the logged-in teacher
                return qs.filter(section__teacher=request.user)
            
            if self.model == Section:
                # Filter the queryset for the logged-in teacher

                group = Group.objects.get(name='مدیر')
                permissions = group.permissions.all()
                permission_list = [permission.id for permission in permissions]


                return qs.filter(teacher=request.user)

        return qs
