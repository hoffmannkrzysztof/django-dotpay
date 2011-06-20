# -*- encoding: utf-8 -*-
from django.conf import settings

try:
    DOTID = getattr(settings, 'DOTID')
except AttributeError:
    raise BaseException("DOTID wymagany")
