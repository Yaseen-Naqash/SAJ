# admin_forms.py (create this file or place inside admin.py)
from django import forms
from a_course_management.models import Section

class SectionSelectionForm(forms.Form):
    section = forms.ModelChoiceField(queryset=Section.objects.all(), label="Select Section")
