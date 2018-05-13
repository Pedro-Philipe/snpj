from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Uf(models.Model):
    codigo_ibge = models.IntegerField(primary_key=True)
    sigla = models.CharField(max_length=2)
    nome_uf = models.CharField(max_length=100)

    def __str__(self):
        return self.sigla

    class Meta:
        ordering = ['sigla']


class Cidade(models.Model):
    codigo_ibge = models.IntegerField(unique=True)
    uf = models.ForeignKey('Uf', to_field='codigo_ibge')
    nome_municipio = models.CharField(max_length=100)
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return self.nome_municipio

    class Meta:
        ordering = ['nome_municipio']


class Usuario(models.Model):
    user = models.OneToOneField(User)
    nome_usuario = models.CharField(max_length=100)
    codigo_ativacao = models.CharField(max_length=12, unique=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Evento(models.Model):
    nome = models.CharField(max_length=100, null=True)  # @TODO remover os campos nulos
    descricao = models.CharField(max_length=255, null=True)
    data = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    usuario = models.ForeignKey(Usuario)
    tipo = models.IntegerField(null=True)
    cpf_assistido = models.CharField(max_length=20, null=True)
    primeira_visita = models.CharField(
        blank=True,
        null=True,
        max_length=1)
    pass


class Assistido(models.Model):
    nome_assistido = models.CharField(max_length=200, null=True)
    representante_legal = models.CharField(max_length=200, null=True)
    rg = models.CharField(max_length=20, null=True)
    cpf = models.CharField(max_length=11, null=True)
    nacionalidade = models.CharField(max_length=200, null=True)
    estado_civil = models.CharField(max_length=200, null=True)
    profissao = models.CharField(max_length=200, null=True)
    renda_familiar = models.CharField(max_length=200, null=True)
    endereco_residencial = models.CharField(max_length=200, null=True)
    endereco_trabalho = models.CharField(max_length=200, null=True)
    cep = models.CharField(max_length=20, null=True)
    telefone_celular = models.CharField(max_length=20, null=True)
    telefone_fixo = models.CharField(max_length=20, null=True)
    telefone_comercial = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200)
    observacoes = models.TextField(null=True)


class Processo(models.Model):
    fatos_narrados = models.TextField(null=True)
    hipossuficiencia = models.FileField(
        upload_to='hipossuficiencia',
        max_length=255,
        blank=True,
        null=True)
    procuracao = models.FileField(
        upload_to='procuracao',
        max_length=255,
        blank=True,
        null=True)


#
# class Processo(models.Model):
#     rg = models.CharField(max_length=100, null=False)
#     cpf = models.ForeignKey(User, to_field='username')
#     tipo = models.ForeignKey(DescricaoProcesso)
#
#
# class DescricaoProcesso(models.Model):
#     descricao = models.CharField(max_length=100, null=False)  # Guarda e divórcio
