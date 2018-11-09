import datetime
from django.db import models
from django.contrib.auth.models import User
from adesao.extra import ContentTypeRestrictedFileField


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



class Evento(models.Model):
    nome = models.CharField(max_length=100, null=True)  # @TODO remover os campos nulos
    descricao = models.CharField(max_length=255, null=True)
    data = models.DateField(null=True)
    hora_inicio = models.TimeField(null=True)
    hora_fim = models.TimeField(null=True)
    usuario = models.ForeignKey(Usuario)
    tipo = models.IntegerField(null=True)
    cpf_assistido = models.CharField(max_length=20, null=True)


class Assistido(models.Model):
    nome = models.CharField(max_length=200, null=True)
    representante_legal = models.CharField(max_length=200)
    rg = models.CharField(max_length=20, null=True)
    cpf = models.CharField(max_length=20, null=True)
    nacionalidade = models.CharField(max_length=200, null=True)
    estado_civil = models.CharField(max_length=50, null=True)
    profissao = models.CharField(max_length=200, null=True)
    renda_familiar = models.CharField(max_length=200, null=True)
    endereco_residencial = models.CharField(max_length=200, null=True)
    endereco_trabalho = models.CharField(max_length=200, null=True)
    cep = models.CharField(max_length=20, null=True)
    telefone_celular = models.CharField(max_length=20, null=True)
    telefone_fixo = models.CharField(max_length=20)
    telefone_comercial = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    observacoes = models.TextField(null=True)
    documentos = models.FileField(
        max_length=255,
        blank=True,
        null=True,
        upload_to='documentos_assistido')

class Processo(models.Model):
    assistido = models.ForeignKey(Assistido)
    tipologia = models.CharField(max_length=50, null=True)
    data = models.DateField(null=True)
    descricao = models.TextField(max_length=1500, null=True)
    status_processo = models.NullBooleanField(null=True)
    usuario = models.ForeignKey(Usuario)
    documentos = models.FileField(
        max_length=255,
        blank=True,
        null=True,
        upload_to='documentos_assistido')
    hora_inicio = models.TimeField(null=True)
    hora_fim = models.TimeField(null=True)
    

    class Meta:
        ordering = ['data']

class Historico(models.Model):
    descricao = models.TextField(max_length=1500, null=True)
    data = models.DateTimeField(auto_now_add=True)
    processo = models.ForeignKey(Processo)

