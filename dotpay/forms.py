from django.forms import ModelForm,IntegerField,URLField,CharField
from dotpay.models import DotRequest
from dotpay.settings import DOTID,DOTURL,DOTURLC,DOTTXTGUZIK

class DotRequestForm(ModelForm):
        id = IntegerField(initial=DOTID)
        URL = URLField(initial=DOTURL)
        typ = IntegerField(initial=0)
        txtguzik = CharField(initial=DOTTXTGUZIK)
        URLC = URLField(initial=DOTURLC)
        
    
        class Meta:
            model = DotRequest