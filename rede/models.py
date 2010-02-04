# -*- coding: utf-8 -*-
from django.db import models
from unicodedata import normalize

class Plano(models.Model):
    """
    Plano de acesso definindo a velocidade de
    download e upload.
    """

    nome = models.CharField(max_length=50)
    download = models.PositiveSmallIntegerField(help_text='Valor em Kbit. Informe um número inteiro que não exceda o total do link.')
    upload = models.PositiveSmallIntegerField(help_text='Valor em Kbit. Informe um número inteiro que não exceda o total do link.')

    class Meta:
        ordering = ['nome']

    def __unicode__(self):
        return self.nome


class PontoRede(models.Model):
    """
    Ponto de Rede presente na rede.
    """

    plano = models.ForeignKey(Plano)
    desc = models.CharField(max_length=100, verbose_name=u'Descrição', unique=True)
    ip = models.IPAddressField(verbose_name='IP', unique=True)
    mac = models.CharField(max_length=18, blank=True, null=True, verbose_name='MAC')
    liberado = models.BooleanField(default=True, verbose_name='Liberado')
    usa_proxy = models.BooleanField(default=True, verbose_name='Usa Proxy?')

    class Meta:
        ordering = ('ip','desc')
        verbose_name = 'ponto de rede'
        verbose_name_plural = 'pontos de rede'

    def __unicode__(self):
        return u'%s' % self.ip

    def save(self):
        desc = self.desc
        self.desc = normalize('NFKD',desc).encode('ASCII','ignore')
        super(PontoRede, self).save()


"""
class InterfaceRede(models.Model):
    TIPO_CHOICES=(
        ('lan','LAN (Rede Interna)'),
        ('wan','WAN (Internet)'),
    )
    iface = models.CharField(max_length=5, verbose_name='Interface', unique=True)
    tipo = models.CharField(max_length=3, choices=TIPO_CHOICES)

    class Meta:
        ordering = ['iface',]
        verbose_name = 'interface de rede'
        verbose_name_plural = 'interfaces de rede'

    def __unicode__(self):
        return self.iface

    def save(self):
        iface = self.iface
        self.iface = iface.lower()
        super(InterfaceRede, self).save()

"""
