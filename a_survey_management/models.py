from django.db import models
from a_course_management.models import Section, SectionStudent
from a_institution_management.models import Branch
# Create your models here.
# SURVEY

# Survey system starts here
class Survey(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='surveys')
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, related_name='surveys')

    class Meta:
        verbose_name = "نظرسنجی" 
        verbose_name_plural = "نظرسنجی ها"

    def __str__(self):
        return f"Survey: {self.title} for {self.section}"


class Question(models.Model):
    TEXT = 'text'
    CHOICE = 'choice'
    SCALE = 'scale'

    QUESTION_TYPES = [
        (TEXT, 'Text'),
        (CHOICE, 'Multiple Choice'),
        (SCALE, 'Scale (1-10)'),
    ]

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES)
    required = models.BooleanField(default=True)

    class Meta:
        verbose_name = "سوال" 
        verbose_name_plural = "سوالات"
    def __str__(self):
        return f"{self.text} ({self.get_question_type_display()})"


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    
    class Meta:
        verbose_name = "گزینه" 
        verbose_name_plural = "گزینه ها"
    def __str__(self):
        return self.text


class Answer(models.Model):
    section_student = models.ForeignKey(SectionStudent, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, null=True, blank=True, on_delete=models.SET_NULL)
    numeric_answer = models.IntegerField(null=True, blank=True)
    text_answer = models.TextField(null=True, blank=True)  # 👈 added for text questions

    class Meta:
        unique_together = ('section_student', 'question')
        verbose_name = "پاسخ" 
        verbose_name_plural = "پاسخ ها"    

    def __str__(self):
        return f"Answer by {self.section_student} to '{self.question.text}'"
    

# A reusable template not tied to a section
class SurveyTemplate(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)



    def create_survey(self, section, title=None):
        survey = Survey.objects.create(
            section=section,
            title=title or self.title,
            is_active=False,
        )
        for t_q in self.template_questions.all():
            q = Question.objects.create(
                survey=survey,
                text=t_q.text,
                question_type=t_q.question_type,
                required=t_q.required,
            )
            if t_q.question_type == 'choice':
                for t_c in t_q.template_choices.all():
                    Choice.objects.create(
                        question=q,
                        text=t_c.text,
                    )
        return survey
    class Meta:
        verbose_name = "نظرسنجی آماده" 
        verbose_name_plural = "نظرسنجی های آماده"
    def __str__(self):
        return f"Template: {self.title}"


class TemplateQuestion(models.Model):
    TEXT = 'text'
    CHOICE = 'choice'
    SCALE = 'scale'

    QUESTION_TYPES = [
        (TEXT, 'Text'),
        (CHOICE, 'Multiple Choice'),
        (SCALE, 'Scale (1-10)'),
    ]

    survey_template = models.ForeignKey(SurveyTemplate, on_delete=models.CASCADE, related_name='template_questions')
    text = models.TextField()
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES)
    required = models.BooleanField(default=True)
    class Meta:
        verbose_name = "سوال آماده" 
        verbose_name_plural = "سوالات آماده"
    def __str__(self):
        return self.text


class TemplateChoice(models.Model):
    template_question = models.ForeignKey(TemplateQuestion, on_delete=models.CASCADE, related_name='template_choices')
    text = models.CharField(max_length=255)


    class Meta:
        verbose_name = "گزینه آماده" 
        verbose_name_plural = "گزینه های آماده"
    def __str__(self):
        return self.text