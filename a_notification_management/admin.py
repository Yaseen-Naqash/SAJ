from django.contrib import admin
from a_notification_management.models import Notification, News
from a_user_management.models import Person
# Register your models here.




@admin.register(News)
class NewsAdmin(admin.ModelAdmin):


        # pre fill the payer field with the sender request data 
    def get_changeform_initial_data(self, request):
        initial_data = super().get_changeform_initial_data(request)
        user_id = request.user.id
        person = Person.objects.get(id=user_id)
        if person:
            initial_data['author'] = person
        return initial_data
    

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):

            # pre fill the payer field with the sender request data 
    def get_changeform_initial_data(self, request):
        initial_data = super().get_changeform_initial_data(request)
        user_id = request.user.id
        person = Person.objects.get(id=user_id)
        if person:
            initial_data['author'] = person
        return initial_data