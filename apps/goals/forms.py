from django import forms
from .models import Goal


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['title', 'target_amount', 'saved_amount', 'note']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Save for a car'}),
            'target_amount': forms.NumberInput(attrs={'step': '0.01'}),
            'saved_amount': forms.NumberInput(attrs={'step': '0.01'}),
            'note': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional note'}),
        }