from django.contrib import admin
from .models import Choice, Question, Survey, Answer, SurveyTemplate, TemplateQuestion, TemplateChoice
# Register your models here.
# SURVEY

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ['title', 'section', 'is_active', 'created_at']
    list_filter = ['section', 'is_active']
    inlines = [QuestionInline]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'survey', 'question_type', 'required']
    list_filter = ['survey', 'question_type']
    inlines = [ChoiceInline]

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['text', 'question']

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['section_student', 'question', 'selected_choice', 'numeric_answer']
    list_filter = ['question__survey']




class TemplateChoiceInline(admin.TabularInline):
    model = TemplateChoice
    extra = 1

class TemplateQuestionInline(admin.TabularInline):
    model = TemplateQuestion
    extra = 1

# @admin.register(SurveyTemplate)
# class SurveyTemplateAdmin(admin.ModelAdmin):
#     list_display = ['title']
#     inlines = [TemplateQuestionInline]

@admin.register(TemplateQuestion)
class TemplateQuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'survey_template', 'question_type']
    inlines = [TemplateChoiceInline]



from django.urls import path
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from .models import SurveyTemplate
from .admin_form import SectionSelectionForm  # import the form
from django.utils.html import format_html
from django.urls import reverse

class SurveyTemplateAdmin(admin.ModelAdmin):
    list_display = ['title','create_survey_link']

    def create_survey_link(self, obj):
        url = reverse('admin:create-survey-from-template', args=[obj.id])
        return format_html('<a class="button" href="{}">Create Survey</a>', url)
    create_survey_link.short_description = "Create Survey"
    create_survey_link.allow_tags = True  # not required in modern Django, but harmless

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        if object_id:
            extra_context['original'] = self.get_object(request, object_id)
        return super().changeform_view(request, object_id, form_url, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:template_id>/create-survey/',
                self.admin_site.admin_view(self.create_survey_view),
                name='create-survey-from-template',
            ),
        ]
        return custom_urls + urls

    def create_survey_view(self, request, template_id):
        template = get_object_or_404(SurveyTemplate, pk=template_id)
        if request.method == 'POST':
            form = SectionSelectionForm(request.POST)
            if form.is_valid():
                section = form.cleaned_data['section']
                template.create_survey(section)
                self.message_user(request, f"Survey created for section: {section}")
                return redirect('admin:a_survey_management_surveytemplate_change', object_id=template_id)
        else:
            form = SectionSelectionForm()
        return render(request, 'admin/create_survey.html', {
            'form': form,
            'title': f"Create Survey from '{template.title}'",
            'template': template,
        })

admin.site.register(SurveyTemplate, SurveyTemplateAdmin)