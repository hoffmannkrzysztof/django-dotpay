# -*- coding: utf-8 -*-

from django.forms import ModelForm
from urllib import urlopen
from dotpay.sms.settings import DOTSMSID
from dotpay.settings import DOTID
from dotpay.sms.models import DotSms

class DotSMSCheckForm(ModelForm):
    
    class Meta:
            model = DotSms
            exclude = ('value',)
    
    def clean(self):
        
        cleaned_data = self.cleaned_data
        try:
            code = cleaned_data["code"]
        except:
            return cleaned_data
        
        page = urlopen("http://dotpay.pl/check_code_fullinfo.php?id=%s&code=%s&type=sms&del=0&check=%s" %(DOTID,DOTSMSID,code) ).read()
        page_split = page.split('\n')
        if int(page_split[0]) == 0:
            self._errors["code"] = self.error_class(['Kod niepoprawny'])
            del cleaned_data["code"]
        elif len(DotSms.objects.filter(code=code)) > 0:
            self._errors["code"] = self.error_class(['Kod został już wykorzystany'])
            del cleaned_data["code"]
        else:
            cleaned_data["value"] = page_split[3]
            self._meta.exclude = None
        
        return cleaned_data
            

        