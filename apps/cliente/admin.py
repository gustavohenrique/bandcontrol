# -*- coding: utf-8 -*-
from django.contrib.admin import site, ModelAdmin

from cliente.models import *
from cliente.forms import ClienteForm

site.register(Bairro)

class ClienteAdmin(ModelAdmin):
    list_display = ('nome','endereco','telefone','celular','inicio_contrato')
    list_filter = ('bairro',)
    search_fields = ['nome',]

    form = ClienteForm
    class Meta:
        model = Cliente


site.register(Cliente, ClienteAdmin)
