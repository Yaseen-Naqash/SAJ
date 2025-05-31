from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Branch
# Register your models here.
admin.site.site_header = "Ahwaz Programming Home"  # Change this to your desired name
admin.site.site_title = "پنل مدیریت"  # Browser tab title
admin.site.index_title = "خوش آمدید به پنل مدیریت"  # Dashboard welcome text




admin.site.register(Branch)

