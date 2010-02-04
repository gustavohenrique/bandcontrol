# -*- coding: utf-8 -*-
"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from django.contrib.admin import AdminSite
from django.http import QueryDict

from rede.admin import *
from rede.models import *


class PontoRedeTest(TestCase):
    def test_exibir_2_pontos_conectados_nao_cadastrados(self):

        ip1 = '192.168.254.254          ether   00:21:91:7b:02:71'
        ip2 = '192.168.254.215          ether   00:08:54:22:6a:94'
        lista_ip = [ip1, ip2]

        p = PontoRedeAdmin(PontoRede, AdminSite)

        resultado_esperado = [{
            'cadastrado': False,
            'desc': u'Máquina não cadastrada',
            'id': 0,
            'ip': '192.168.254.254',
            'liberado': False,
            'mac': '00:21:91:7b:02:71',
            'plano': '',
            'usa_proxy': True
        }, {
            'cadastrado': False,
            'desc': u'Máquina não cadastrada',
            'id': 0,
            'ip': '192.168.254.215',
            'liberado': False,
            'mac': '00:08:54:22:6a:94',
            'plano': '',
            'usa_proxy': True
        }]

        self.failUnlessEqual(resultado_esperado, p._montar_lista_conectados(lista_ip))


    def test_cadastrar_ponto_conectado(self):

        # Cadastra o plano inicial para ter id=1
        plano = Plano.objects.create(nome='128k',download=128,upload=64).save()

        dados = QueryDict('desc=gateway&ip=192.168.254.254&mac=00:21:91:7b:02:71&plano=1')

        p = PontoRedeAdmin(PontoRede, AdminSite)
        self.assertEquals(u'ok', p._cadastrar_ponto_conectado(dados))

        # Verifica se foi liberado e definido para usar proxy por padrao
        ponto = PontoRede.objects.get(id=1)
        self.assertEquals([True, True], [ponto.liberado, ponto.usa_proxy])




__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True
"""}

