from django.db import models
from django.contrib.auth.models import User

# from smart_selects.db_fields import ChainedForeignKey

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
