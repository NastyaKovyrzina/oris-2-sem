from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import GlitchProfile, Anomaly

class RegistrationForm(UserCreationForm):
    nickname = forms.CharField(max_length=100, label="Никнейм")
    bio = forms.CharField(widget=forms.Textarea, label="О себе", required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'nickname', 'bio']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Создаём профиль
            GlitchProfile.objects.create(
                user=user,
                nickname=self.cleaned_data['nickname'],
                bio=self.cleaned_data['bio'],
                belief_level=50
            )
        return user

class AnomalyForm(forms.ModelForm):
    class Meta:
        model = Anomaly
        fields = ['title', 'description', 'location', 'danger_level']