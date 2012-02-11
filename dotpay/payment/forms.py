from django.forms import ModelForm,IntegerField,URLField,CharField
from dotpay.payment.models import DotRequest
from dotpay.payment.settings import DOTURL,DOTURLC,DOTTXTGUZIK
from dotpay.settings import DOTID
from django.forms.fields import HiddenInput
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from urlparse import urljoin, urlparse


class DotRequestForm(ModelForm):
        id = IntegerField(initial=DOTID,widget=HiddenInput)
        URL = URLField(initial=DOTURL,widget=HiddenInput)
        typ = IntegerField(initial=0,widget=HiddenInput)
        txtguzik = CharField(initial=DOTTXTGUZIK,widget=HiddenInput)
        URLC = URLField(initial=DOTURLC,widget=HiddenInput)
        lang = CharField(max_length=2,initial='pl',widget=HiddenInput)
        kraj = CharField(max_length=3,initial='POL',widget=HiddenInput)
        
    
        class Meta:
            model = DotRequest
            widgets = {
            'kwota' : HiddenInput,
            'opis' : HiddenInput,
            'control' : HiddenInput,
            'email' : HiddenInput,
            }
