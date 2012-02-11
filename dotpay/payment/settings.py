# -*- encoding: utf-8 -*-
from django.conf import settings

try:
    DOTPIN = getattr(settings, 'DOTPIN')
except AttributeError:
    raise BaseException("DOTPIN wymagany")

try:
    DOTURL  = getattr(settings, 'DOTURL')
except AttributeError:
    raise BaseException("DOTURL wymagany")

try:
    DOTURLC  = getattr(settings, 'DOTURLC')
except AttributeError:
    raise BaseException("DOTURLC wymagany")

DOTTXTGUZIK  = getattr(settings, 'DOTTXTGUZIK', 'Powrót do sklepu')

