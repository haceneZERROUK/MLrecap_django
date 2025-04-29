from django import forms

class ContactForm(forms.Form):
    nom = forms.CharField(label='Nom complet', max_length=100)
    email = forms.EmailField(label='Email')
    message = forms.CharField(label='Message', widget=forms.Textarea)
