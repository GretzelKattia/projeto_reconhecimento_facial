from django import forms
from .models import Funcionario

class FuncionarioForm(forms.ModelForm):
    """Formulário para os dados básicos do funcionário."""
    class Meta:
        model = Funcionario
        fields = ['nome', 'cpf', 'nivel_acesso', 'divisao']

class UserForm(forms.Form):
    """Formulário para os dados do usuário (login)."""
    username = forms.CharField(max_length=150, label="Nome de Usuário")
    password = forms.CharField(widget=forms.PasswordInput, label="Senha")

class ColetaDeFacesForm(forms.Form):
    """Formulário para a imagem do rosto."""
    image = forms.ImageField(label="Foto do Rosto")