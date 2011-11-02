# -*- encoding: utf-8 -*-
from django.conf import settings
from django.contrib.sites.models import Site
from urlparse import urljoin
from django.core.urlresolvers import reverse

try:
    DOTPIN = getattr(settings, 'DOTPIN')
except AttributeError:
    raise BaseException("DOTPIN wymagany")

try:
    DOTURL  = getattr(settings, 'DOTURL')
except AttributeError:
    raise BaseException("DOTURL wymagany")

try:
    site = Site.objects.get_current()
    domain = site.domain
    if domain.startswith("http://"):
        DOTURLC = urljoin(domain,reverse('dotpay_receiver'))
    else:
        DOTURLC = urljoin("http://"+domain,reverse('dotpay_receiver'))
except AttributeError:
    raise BaseException("DOTURLC wymagany. Błąd SITE.")

DOTTXTGUZIK  = getattr(settings, 'DOTTXTGUZIK', 'Powrót do sklepu')
