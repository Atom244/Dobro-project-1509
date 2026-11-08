from django import forms
from .models import Appeal, AppealCategory


class AppealForm(forms.ModelForm):
    class Meta:
        model = Appeal
        fields = ['category', 'subject', 'description', 'address', 'attachment']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6}),
            'attachment': forms.ClearableFileInput(attrs={'accept': '.pdf,.jpg,.jpeg,.png,.doc,.docx'}),
        }

    def clean_attachment(self):
        file = self.cleaned_data.get('attachment')
        if file and file.size > 5 * 1024 * 1024:
            raise forms.ValidationError('Размер файла не должен превышать 5 МБ.')
        return file
