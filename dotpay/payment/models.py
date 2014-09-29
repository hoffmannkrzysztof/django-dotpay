# -*- coding: utf-8 -*-
import os
from django.db import models
import hashlib
import random
from dotpay.payment.util import  TRANS_STATUS_CHOICES,STATUS_CHOICES, generate_md5
from dotpay.payment.signals import dot_anulowana,dot_error,dot_nowa,dot_odmowa,dot_reklamacja,dot_wykonana
import time

class DotRequest(models.Model):
    id_request = models.AutoField(primary_key=True)
    kwota = models.DecimalField(max_digits=5, decimal_places=2, help_text=u"Kwota transakcji  podana z częścią setną.")
    opis = models.CharField(max_length=255,help_text=u"Opis przeprowadzanej transakcji. ")
    control = models.CharField(max_length=128,help_text=u"Parametr kontrolny",unique=True)
    email = models.EmailField()
    added = models.DateTimeField(u"Data zamówienia",auto_now_add=True,help_text="Data zamówienia")
    
    class Meta:
        verbose_name = u'Dotpay akcja'
        verbose_name_plural = u'Dotpay akcje'
    
    def __unicode__(self):
        return u"%s" % self.opis
    
    def save(self,*args, **kwargs):
        self._gen_control()
        super(DotRequest, self).save(*args, **kwargs)
        
    def get_status(self):
        if self.dotresponse_set.count() > 0:
            status = self.dotresponse_set.order_by("-t_status").all()[0]
            return status.get_t_status_display()
        else:
            return u"Nowa"
    
    def _gen_control(self):
        nonce = ''.join([str(self.kwota), str(time.time()), os.urandom(1024)])
        self.control = hashlib.md5(nonce).hexdigest()


class DotResponse(models.Model):
    id_response = models.AutoField(primary_key=True)
    id = models.PositiveIntegerField(help_text="ID konta w systemie Dotpay, na rzecz którego dokonywana jest płatność (ID konta Sprzedawcy)")
    status = models.CharField(max_length=4, choices=TRANS_STATUS_CHOICES,help_text="Informacja o ewentualnym wystąpieniu błędów na stronach serwisu Dotpay")
    control = models.CharField(max_length=128,help_text="Parametr kontrolny jeżeli został podany podczas przekazywania kupującego na strony serwisu Dotpay")
    t_id = models.CharField(max_length=100,help_text="Numer  identyfikacyjny transakcji nadany po księgowaniu na koncie użytkownika Dotpay (Sprzedawcy).")
    amount = models.DecimalField(max_digits=5, decimal_places=2, help_text="Kwota transakcji. Separatorem dziesiętnym jest znak kropki.")
    orginal_amount = models.CharField(max_length=100,help_text="Kwota transakcji i znacznik waluty (oddzielone znakiem spacji). Separatorem dziesiętnym jest znak kropki")
    email = models.CharField(max_length=100,help_text="Adres email osoby dokonującej płatność.")
    t_status = models.CharField(max_length=1,choices=STATUS_CHOICES)
    description = models.CharField(max_length=255,null=True,blank=True,help_text="Pełna treść opisu transakcji.")
    md5 = models.CharField(max_length=32)    
    t_date = models.DateTimeField(auto_now_add=True,help_text="Data otrzymania komunikatu")
    request = models.ForeignKey(DotRequest,help_text="FK dla requestu")
    
    class Meta:
        verbose_name = u'Dotpay odpowiedź'
        verbose_name_plural = u'Dotpay odpowiedzi'
        unique_together = (('t_id', 'control'),)
    
    def __unicode__(self):
        return u"%s - %s" % (self.request.opis,self.status)

    def _gen_md5(self):
        return generate_md5(self.control, self.t_id, self.amount, self.t_status, self.email)

    def _check_md5(self):
        return bool(self._gen_md5() == self.md5)
    
    def save(self,*args, **kwargs):
        self.request = DotRequest.objects.get(control=self.control)
        if self._check_md5():

            super(DotResponse, self).save(*args, **kwargs)
            if self.t_status == '2': #WYKONANA
                dot_wykonana.send(sender=self)
            elif self.t_status == '1': #NOWA
                dot_nowa.send(sender=self)
            elif self.t_status == '3': #ODMOWA
                dot_odmowa.send(sender=self)
            elif self.t_status == '4': #ANULOWANA
                dot_anulowana.send(sender=self)
            elif self.t_status == '5': #REKLAMACJA
                dot_reklamacja.send(sender=self)
            else:
                dot_error.send(sender=self)
                raise BaseException("STATUS Not implemented:"+str(self.t_status))
        else:
            dot_error.send(sender=self)
            raise BaseException("MD5 INCORRECT. id_response: %d id: %d" % self.id_response,self.id)
