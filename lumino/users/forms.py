from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms

from .models import Profile


#
# class EditProfileForm(forms.ModelForm):
#    class Meta:
#        model = Profile
#        fields = ['avatar', 'bio']
#        widgets = {
#            'bio': forms.Textarea(
#                attrs={
#                    'type': 'string',
#                }
#            ),
#        }
#
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.attrs = dict(novalidate=True)

        self.helper.layout = Layout(
            'avatar',
            FloatingField('bio'),
            Submit('save', 'Save', css_class='btn-info w-100 mt-2 mb-2'),
        )

    def save(self, *args, **kwargs):
        profile = super().save(commit=False)
        if not profile.avatar:
            profile.avatar = '../media/avatars/noavatar.png'
        profile = super().save(*args, **kwargs)
        return profile
