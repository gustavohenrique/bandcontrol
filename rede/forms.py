# -*- coding: utf-8 -*-
from django.forms import fields, Field, TextInput
from django.forms.forms import ValidationError
from django.forms.models import ModelForm

from rede.models import *


class MACField(Field):
    """
    Verifica se o MAC informado está no formato XX:XX:XX:XX:XX:XX
    """

    def clean(self, value):
        mac = value
        if mac and len(mac) != 17:
            raise ValidationError('MAC deve conter 17 caracteres.')
        elif mac:
            if len(mac.split(':')) != 6:
                raise ValidationError('MAC deve ser separado por dois pontos (:).')
        return mac
            
            
class PontoRedeForm(ModelForm):
    mac = MACField(label='MAC', widget=TextInput(attrs={'maxlength':17}))

    class Meta:
        model = PontoRede
