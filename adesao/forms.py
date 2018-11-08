from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.crypto import get_random_string
from django.forms import ModelForm
from django.template.defaultfilters import filesizeformat

from .models import Usuario, Evento, Assistido, Processo
from .utils import validar_cpf, validar_cnpj, limpar_mascara
import re
import pdb

content_types = [
    'image/png',
    'image/jpg',
    'image/jpeg',
    'application/pdf',
    'application/msword',
    'application/vnd.oasis.opendocument.text',
    'application/vnd.openxmlformats-officedocument.' +
    'wordprocessingml.document',
    'application/x-rar-compressed',
    'application/zip',
    'application/octet-stream',
    'text/plain']


class RestrictedFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop("content_types")
        self.max_upload_size = kwargs.pop("max_upload_size")

        super(RestrictedFileField, self).__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        file = super(RestrictedFileField, self).clean(data, initial)

        try:
            content_type = file.content_type
            if content_type in self.content_types:
                if file._size > self.max_upload_size:
                    raise forms.ValidationError(
                        'O arquivo deve ter menos de %s. Tamanho atual %s'
                        % (filesizeformat(self.max_upload_size),
                            filesizeformat(file._size)))
            else:
                raise forms.ValidationError(
                    'Arquivos desse tipo não são aceitos.')
        except AttributeError:
                pass

        return data
class CadastrarAssistidoForm(forms.ModelForm):
    nome = forms.CharField(max_length=14, required=True)
    representante_legal = forms.CharField(max_length=150)
    rg = forms.CharField(max_length=20, required=True)
    cpf = forms.CharField(max_length=20, required=True)
    nacionalidade = forms.CharField(max_length=200, required=True)
    estado_civil = forms.CharField(max_length=50, required=True)
    profissao = forms.CharField(max_length=200, required=True)
    renda_familiar = forms.CharField(max_length=200, required=True)
    endereco_residencial = forms.CharField(max_length=200, required=True)
    endereco_trabalho = forms.CharField(max_length=200)
    cep = forms.CharField(max_length=20, required=False)
    telefone_celular = forms.CharField(max_length=20, required=False)
    telefone_fixo = forms.CharField(max_length=20)
    telefone_comercial = forms.CharField(max_length=200)
    email = forms.EmailField(max_length=200)
    observacoes = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = Assistido
        fields = ('nome', 'representante_legal', 'rg', 'cpf', 'nacionalidade', 'estado_civil', 'profissao', 'renda_familiar', 'endereco_residencial', 'endereco_trabalho',
                  'cep', 'telefone_celular', 'telefone_fixo', 'telefone_comercial', 'email', 'observacoes')

    def clean_email(self):
        try:
            Assistido.objects.get(email=self.cleaned_data['email'])
            raise forms.ValidationError('Este e-mail já foi cadastrado!')
        except Assistido.DoesNotExist:
            return self.cleaned_data['email']

    def clean_cpf(self):
        if not validar_cpf(self.cleaned_data['cpf']):
            raise forms.ValidationError('Por favor, digite um CPF válido!')

        usuario_mesmo_cpf = Assistido.objects.filter(cpf=self.cleaned_data['cpf'])

        if usuario_mesmo_cpf.count() == 0:
            raise forms.ValidationError('É necessário iniciar o cadastro do CPF gerando um evento')

        return self.cleaned_data['cpf']

    def save(self, commit=True, *args, **kwargs):
        assistido = super(CadastrarAssistidoForm, self).save(commit=False)

        assistido = Assistido.objects.get(cpf=self.cleaned_data['cpf'])
        assistido.representante_legal = self.cleaned_data['representante_legal']
        assistido.endereco_residencial = self.cleaned_data['endereco_residencial']
        assistido.cep = self.cleaned_data['cep']
        assistido.email = self.cleaned_data['email']
        assistido.endereco_trabalho = self.cleaned_data['endereco_trabalho']
        assistido.estado_civil = self.cleaned_data['estado_civil']
        assistido.nacionalidade = self.cleaned_data['nacionalidade']
        assistido.observacoes = self.cleaned_data['observacoes']
        assistido.profissao = self.cleaned_data['profissao']
        assistido.renda_familiar = self.cleaned_data['renda_familiar']
        assistido.rg = self.cleaned_data['rg']
        assistido.telefone_celular = self.cleaned_data['telefone_celular']
        assistido.telefone_comercial = self.cleaned_data['telefone_comercial']
        assistido.telefone_fixo = self.cleaned_data['telefone_fixo']
        assistido.nome = self.cleaned_data['nome']


        if commit:
            assistido.save()

        return assistido
        

    # def clean_telefone_celular(self):
    #     if (self.cleaned_data['telefone_celular']):
    #         raise forms.ValidationError('Por favor, digite um CELULAR válido!')
    #
    #     usuario_mesmo_telefone_celular = Assistido.objects.filter(telefone_celular=self.cleaned_data['telefone_celular'])
    #
    #     return self.cleaned_data['telefone_celular']

    # def clean_rg(self):
    #     if not validar_cpf(self.cleaned_data['rg']):
    #         raise forms.ValidationError('Por favor, digite um RG válido!')
    #
    #     usuario_mesmo_rg = Assistido.objects.filter(rg=self.cleaned_data['rg'])
    #
    #     if usuario_mesmo_rg.count() > 0:
    #         raise forms.ValidationError('RG já cadastrado!')
    #
    #     return self.cleaned_data['rg']

class CadastroProcessoForm(forms.ModelForm):
    cpf_assistido = forms.CharField(max_length=20, required=True)
    tipologia = forms.CharField(required=True)
    data = forms.DateField()
    descricao = forms.CharField(max_length=1500, widget=forms.Textarea(), required=True)
    status_processo = forms.CharField(max_length=20, required=True)
    responsavel_processo = forms.CharField(max_length=50, required=True)

    class Meta:
        model = Processo
        fields = ('cpf_assistido', 'tipologia', 'data', 'descricao', 'status_processo', 'responsavel_processo')

    def clean_cpf(self):
        if not validar_cpf(self.cleaned_data['cpf_assistido']):
            raise forms.ValidationError('Por favor, digite um CPF válido!')

        usuario_mesmo_cpf = Assistido.objects.filter(cpf_assistido=self.cleaned_data['cpf_assistido'])

        if usuario_mesmo_cpf.count() == 0:
            raise forms.ValidationError('CPF não cadastrado no sistema')

        return self.cleaned_data['cpf_assistido']

class CadastrarUsuarioForm(UserCreationForm):
    username = forms.CharField(max_length=14, required=True)
    confirmar_email = forms.EmailField(required=True)
    email = forms.EmailField(required=True)
    nome_usuario = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def clean_confirmar_email(self):
        if self.data.get('email') != self.cleaned_data['confirmar_email']:
            raise forms.ValidationError(
                'Confirmação de e-mail não confere.')

        return self.cleaned_data['confirmar_email']

    def clean_email(self):
        try:
            User.objects.get(email=self.cleaned_data['email'])
            raise forms.ValidationError('Este e-mail já foi cadastrado!')
        except User.DoesNotExist:
            return self.cleaned_data['email']

    def clean_username(self):
        if not validar_cpf(self.cleaned_data['username']):
            raise forms.ValidationError('Por favor, digite um CPF válido!')

        try:
            User.objects.get(username=''.join(re.findall(
                '\d+',
                self.cleaned_data['username'])))
            raise forms.ValidationError('Esse CPF já foi cadastrado.')
        except User.DoesNotExist:
            return self.cleaned_data['username']

        return self.cleaned_data['username']

    def save(self, commit=True):
        user = super(CadastrarUsuarioForm, self).save(commit=False)
        user.username = limpar_mascara(self.cleaned_data['username'])
        user.email = self.cleaned_data['email']
        user.is_active = False
        if commit:
            user.save()

        usuario = Usuario()
        usuario.user = user
        usuario.nome_usuario = self.cleaned_data['nome_usuario']
        codigo_ativacao = get_random_string()
        usuario.codigo_ativacao = codigo_ativacao
        if commit:
            usuario.save()

        return user


class CadastrarEventosForm(ModelForm):
    class Meta:
        model = Evento
        fields = '__all__'

    def clean_cpf_assistido(self):
        if not validar_cpf(self.cleaned_data['cpf_assistido']):
            raise forms.ValidationError('Por favor, digite um CPF válido!')

        usuario_mesmo_cpf = Assistido.objects.filter(cpf=self.cleaned_data['cpf_assistido'])

        if usuario_mesmo_cpf.count() > 0:
            raise forms.ValidationError('CPF já cadastrado!')

        return self.cleaned_data['cpf_assistido']

    def clean(self):
        super(CadastrarEventosForm, self).clean()
        if self.cleaned_data['hora_fim'] <= self.cleaned_data['hora_inicio']:
             self.add_error('hora_fim', 'O horário de fim precisa ser maior que o de início.')

    def save(self, commit=True, *args, **kwargs):
        form = super(CadastrarEventosForm, self).save(commit=False)
        usuario_mesmo_cpf = Assistido.objects.filter(cpf=self.cleaned_data['cpf_assistido'])

        if usuario_mesmo_cpf.count() == 0:
            assistido = Assistido()
            assistido.cpf = self.cleaned_data['cpf_assistido']

            evento = Evento()
            evento.nome = self.cleaned_data['nome']
            evento.hora_inicio = self.cleaned_data['hora_inicio']
            evento.hora_fim = self.cleaned_data['hora_fim']
            evento.data = self.cleaned_data['data']
            evento.usuario_id = self.cleaned_data['usuario'].id
            evento.tipo = self.cleaned_data['tipo']
            evento.cpf_assistido = self.cleaned_data['cpf_assistido']
            evento.descricao = self.cleaned_data['descricao']

            if commit:
                evento.save()
                assistido.save()
        return form