from django import forms
from core.models import File


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file']

    def clean_file(self):
        file = self.cleaned_data['file']
        if not file.name.endswith('.py'):
            raise forms.ValidationError(
                'The file must have the extension ".py"'
            )
        return file
