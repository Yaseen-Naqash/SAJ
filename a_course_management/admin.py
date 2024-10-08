from django.contrib import admin
from .models import Course, Section, SectionTimeSlot, Exam, HomeWork, HomeWorkDocument, ExamDocument, Degree
# Register your models here.
admin.site.register(SectionTimeSlot)

from django.contrib import admin
from .models import Course, Section

class SectionInline(admin.TabularInline):  # or use admin.StackedInline for a different layout
    model = Section
    extra = 1  # Number of empty sections to display

class SectionTimeSlotInline(admin.TabularInline):  # or use admin.StackedInline
    model = SectionTimeSlot
    extra = 1  # Number of empty time slots to display

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    inlines = [SectionTimeSlotInline]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [SectionInline]


admin.site.register(Degree)
admin.site.register(Exam)

admin.site.register(ExamDocument)

admin.site.register(HomeWork)
admin.site.register(HomeWorkDocument)


