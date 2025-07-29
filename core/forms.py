from django import forms
from .models import Commande

class CommandeForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = ['nom_client', 'adresse_livraison', 'telephone']
        widgets = {
            'nom_client': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse_livraison': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
        }
