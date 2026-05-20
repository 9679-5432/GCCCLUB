from django import forms
from .models import Player, Registration


class PlayerForm(forms.ModelForm):

    class Meta:
        model = Player
        fields = '__all__'


class RegistrationForm(forms.ModelForm):

    class Meta:
        model = Registration
        fields = '__all__'