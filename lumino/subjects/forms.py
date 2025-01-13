from crispy_bootstrap5.bootstrap5 import Field, FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Layout, Row, Submit
from django import forms

from .models import Enrollment, Lesson, Subject


class AddLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.attrs = dict(novalidate=True)

        self.helper.layout = Layout(
            FloatingField('title'),
            Field('content'),
            Submit('save', 'Save', css_class='btn-info w-100 mt-2 mb-2'),
        )


class EditLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.attrs = dict(novalidate=True)

        self.helper.layout = Layout(
            FloatingField('title'),
            Field('content'),
            Submit('save', 'Save', css_class='btn-info w-100 mt-2 mb-2'),
        )


class EnrollForm(forms.Form):
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(), widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subjects'].queryset = self.fields['subjects'].queryset.exclude(
            pk__in=user.students_subjects.all()
        )

        self.helper = FormHelper()

        self.helper.attrs = dict(novalidate=True)

        self.helper.layout = Layout(
            Field('subjects'),
            Submit('enroll', 'Enroll', css_class='btn-info w-100 mt-2 mb-2'),
        )

    def save(self, user, *args, **kwargs):
        for subject1 in self.cleaned_data['subjects']:
            Enrollment.objects.create(student=user, subject=subject1)


class UnenrollForm(forms.Form):
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(), widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subjects'].queryset = self.fields['subjects'].queryset.filter(
            pk__in=user.students_subjects.all()
        )

        self.helper = FormHelper()

        self.helper.attrs = dict(novalidate=True)

        self.helper.layout = Layout(
            Field('subjects'),
            Submit('unenroll', 'Unenroll', css_class='btn-info w-100 mt-2 mb-2'),
        )

    def save(self, user, *args, **kwargs):
        for subject1 in self.cleaned_data['subjects']:
            Enrollment.objects.get(student=user, subject=subject1).delete()


class EditMarkForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['mark']


class EditMarkFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_show_labels = False
        self.layout = Layout(
            Row(
                HTML(
                    '{% load subject_extras %} <div class="col-md-2">{% student_label formset forloop.counter0 %}</div>'
                ),
                Field('mark', wrapper_class='col-md-2'),
                css_class='align-items-baseline',
            )
        )
        self.add_input(Submit('save', 'Save marks', css_class='mt-3'))
