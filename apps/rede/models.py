# -*- coding: utf-8 -*-
from django.db import models
from unicodedata import normalize
#from django.template.defaultfilters import slugify

from cliente.models import Cliente


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


class Servidor(models.Model):
    """
    Servidor entre o gateway e a internet.
    """

    INTERFACE_CHOICES = (
        ('eth0','eth0'),
        ('eth1','eth1'),
        ('eth2','eth2'),
        ('eth3','eth3'),
        ('wlan0','wlan0'),
        ('wlan1','wlan1'),
        ('wlan2','wlan2'),
    )

    nome = models.SlugField(max_length=100, unique=True)
    ip = models.IPAddressField(verbose_name='IP', unique=True)
    interface_rede = models.CharField(max_length=5, choices=INTERFACE_CHOICES, verbose_name=u'Interface de Rede')

    class Meta:
        verbose_name_plural = 'servidores'

    def __unicode__(self):
        return self.ip


class AccessPoint(models.Model):
    """
    Ponto de acesso o qual cada IP cliente está conectado.
    """

    nome = models.SlugField(max_length=100, unique=True)
    ip = models.IPAddressField(verbose_name='IP', unique=True)
    local = models.SlugField(max_length=100)

    class Meta:
        verbose_name_plural = 'access point'

    def __unicode__(self):
        return self.nome


class PontoRede(models.Model):
    """
    Ponto de Rede presente na rede.
    """

    cliente = models.ForeignKey(Cliente, blank=True, null=True)
    servidor =  models.ForeignKey(Servidor, blank=True, null=True, verbose_name=u'Rota padrão')
    ap =  models.ForeignKey(AccessPoint, blank=True, null=True)
    plano = models.ForeignKey(Plano)
    desc = models.CharField(max_length=100, verbose_name=u'Descrição', blank=True, null=True)
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
        if self.cliente:
            nova_desc = self.cliente.nome
        else:
            nova_desc = normalize('NFKD',self.desc).encode('ASCII','ignore')

        self.desc = nova_desc
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
