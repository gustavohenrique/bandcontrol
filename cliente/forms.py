# -*- coding: utf-8 -*-
from django.forms.models import ModelForm
from django.contrib.localflavor.br.forms import BRPhoneNumberField

from cliente.models import Cliente


class ClienteForm(ModelForm):
    telefone = BRPhoneNumberField(label='Telefone', required=False, help_text=u'Ex.: 00-0000-0000')
    celular = BRPhoneNumberField(label='Celular', required=False, help_text=u'Ex.: 00-0000-0000')

    class Meta:
        model = Cliente
