from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Post, Resposta
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserCreationForm(forms.ModelForm):
    senha1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    senha2 = forms.CharField(label='Confirme a senha', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)
    
    def clean_senha2(self):
        """Validação do campo de confirmação de senha.

        O nome deve ser 'clean_<fieldname>' para que o Django o execute
        automaticamente durante a validação do formulário.
        """
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

class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    list_display = ('email', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    fieldsets = (
        # 'password' é o nome correto do campo do AbstractBaseUser
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'senha1', 'senha2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'criado_em')
    search_fields = ('titulo', 'conteudo')

@admin.register(Resposta)
class RespostaAdmin(admin.ModelAdmin):
    list_display = ('post', 'autor', 'criado_em')

admin.site.register(User, UserAdmin)