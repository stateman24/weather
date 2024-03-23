from django import forms
from .models import City

class CityForm(forms.ModelForm):
    
    class Meta:
        model = City
        fields = ('name', 'country')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'h-12 min-w-[12rem] rounded-lg border-emerald-500 indent-4 text-emerald-900 shadow-lg focus:outline-none focus:ring focus:ring-emerald-600',
                'placeholder':"e.g London,....," 
            }),
            'country': forms.TextInput(attrs={
                'class': 'h-12 min-w-[12rem] rounded-lg border-emerald-500 indent-4 text-emerald-900 shadow-lg focus:outline-none focus:ring focus:ring-emerald-600',
                'placeholder':"e.g NG,US,GH,....," 
            }),
        }

