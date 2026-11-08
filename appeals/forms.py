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
        labels = {
            'category': 'Категория обращения',
            'subject': 'Тема обращения',
            'description': 'Описание проблемы',
            'address': 'Адрес проблемы',
            'attachment': 'Вложение',
        }
        help_texts = {
            'description': 'Опишите ситуацию подробно: что произошло и когда.',
            'address': 'Укажите адрес, если проблема связана с конкретным местом.',
            'attachment': 'Необязательно, до 5 МБ: PDF, JPG, PNG, DOC или DOCX.',
        }

    def clean_attachment(self):
        file = self.cleaned_data.get('attachment')
        if file and file.size > 5 * 1024 * 1024:
            raise forms.ValidationError('Размер файла не должен превышать 5 МБ.')
        return file
