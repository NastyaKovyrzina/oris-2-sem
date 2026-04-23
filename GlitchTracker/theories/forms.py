from django import forms
from .models import Theory
import re

class TheoryForm(forms.ModelForm):
    class Meta:
        model = Theory
        fields = ['title', 'explanation']   # только поля, которые вводит пользователь
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название теории'}),
            'explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Ваше объяснение...'}),
        }
        labels = {
            'title': 'Заголовок теории',
            'explanation': 'Объяснение',
        }

class TheoryForm(forms.ModelForm):
    class Meta:
        model = Theory
        fields = ['title', 'explanation']

    def clean_title(self):
        title = self.cleaned_data['title']
        # Запрещённые слова
        bad_words = ['дурак', 'идиот', 'мат', 'редиска']
        for word in bad_words:
            if re.search(rf'\b{word}\b', title, re.IGNORECASE):
                raise forms.ValidationError(f"Заголовок содержит запрещённое слово: {word}")
        return title