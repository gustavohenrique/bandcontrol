# -*- coding: utf-8 -*-
from django.conf import settings
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def boolean_icon(field_val):
    BOOLEAN_MAPPING = {True: 'yes', False: 'no', None: 'unknown'}
    return mark_safe(u'<img src="%simg/admin/icon-%s.gif" alt="%s" />' % (settings.ADMIN_MEDIA_PREFIX, BOOLEAN_MAPPING[field_val], field_val))

