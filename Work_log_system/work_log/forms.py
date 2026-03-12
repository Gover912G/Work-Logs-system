from django import forms
from .models import WorkLog

class WorkLogForm(forms.ModelForm):

    class Meta:
        model = WorkLog
        fields = [
        
            'task',
            'location',
            'problem',
            'solution',
            'status',
            'remarks'
        ]

        widgets = {
            # 'date': forms.DateInput(attrs={'type': 'date'}),
            'task': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'problem': forms.Textarea(attrs={'rows':3 , 'class': 'form-control'}),
            'solution': forms.Textarea(attrs={'rows':3, 'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'rows':2, 'class': 'form-control'}),
        }