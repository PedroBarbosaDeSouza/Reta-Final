from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()

class SignUpForm(forms.ModelForm):
    senha1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    senha2 = forms.CharField(label='Confirme a senha', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')
    
    def limpa_senha2(self):
        s1 = self.cleaned_data.get("senha1")
        s2 = self.cleaned_data.get("senha2")
        if s1 and s2 and s1 != s2:
            raise forms.ValidationError("As senhas não conferem.")
        return s2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["senha1"])
        if commit:
            user.save()
        return user