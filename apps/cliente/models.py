# -*- coding: utf-8 -*-
from django.db import models
from unicodedata import normalize


class Bairro(models.Model):
    nome = models.CharField(max_length=50)

    def __unicode__(self):
        return self.nome


class Cliente(models.Model):
    bairro = models.ForeignKey(Bairro)
    nome = models.CharField(max_length=250)
    logradouro = models.CharField(max_length=250)
    numero = models.CharField(max_length=10)
    telefone = models.CharField(max_length=12, blank=True, null=True)
    celular = models.CharField(max_length=12, blank=True, null=True)
    inicio_contrato = models.DateField(verbose_name='Início do Contrato')

    def __unicode__(self):
        return self.nome

    def save(self):
        """
        Converte o nome para maiusculo e retira acentos.
        """

        if self.nome:
            nome_formatado = normalize('NFKD',self.nome).encode('ASCII','ignore')
            self.nome = nome_formatado.upper()
            super(Cliente, self).save()

    @property
    def endereco(self):
        """
        Retorna logradouro, numero e o bairro
        """

        return '%s, %s - %s' % (self.logradouro, self.numero, self.bairro)
