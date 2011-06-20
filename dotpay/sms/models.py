# -*- coding: utf-8 -*-
from django.db import models
from dotpay.sms.signals import dot_sms_ok

class DotSms(models.Model):
    code = models.CharField(unique=True,max_length=8,verbose_name="Kod",help_text="Kod autoryzacyjny")   
    value = models.DecimalField(max_digits=5, decimal_places=1,verbose_name="Wartość",help_text="Wartość netto ceny sms'a")
    added = models.DateTimeField("Data zamówienia",auto_now_add=True)
    
    class Meta:
        verbose_name = 'Dotpay sms'
        verbose_name_plural = 'Dotpay smsy'
    
    def save(self,*args, **kwargs):
        super(DotSms, self).save(*args, **kwargs)
        dot_sms_ok.send(sender=self)
    
    def __unicode__(self):
        return u"%s : %s" % (self.code,self.value)