# -*- encoding: utf-8 -*-
from django.conf import settings

try:
    DOTSMSID = getattr(settings, 'DOTSMSID') #Identyfikator usługi AP.XXXX
except AttributeError:
    raise BaseException("DOTSMSID wymagany")