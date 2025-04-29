from django import forms
from django.contrib.auth import get_user_model

class ContactForm(forms.Form):
    nom = forms.CharField(label='Nom complet', max_length=100)
    email = forms.EmailField(label='Email')
    message = forms.CharField(label='Message', widget=forms.Textarea)


User = get_user_model()

class GuestUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_superuser = False
        user.is_staff = True
        if commit:
            user.save()
        return user

