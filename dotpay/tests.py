# -*- coding: utf-8 -*-

from django.utils import unittest
from dotpay.models import DotResponse, DotRequest
from dotpay.settings import DOTID
from datetime import datetime
from django.test.client import RequestFactory

from dotpay.util import generate_md5,STATUS_CHOICES, DOTPAY_SERVERS
from dotpay.views import receiver
from dotpay.signals import dot_wykonana, dot_anulowana, dot_odmowa, dot_nowa,\
    dot_reklamacja
from django import dispatch

signal_count = 0


class DotPayTest(unittest.TestCase):
    def setUp(self):
        
        self.param = {}
        self.param['kwota'] = 24.33
        self.param['opis'] = 'Testowe zamówienie #1'
        self.param['email'] = 'krzysiekpl@gmail.com'
        self.param['t_id'] = 'TST-20102'
        
        dotrequest = DotRequest(kwota=self.param['kwota'],
                                  opis=self.param['opis'],
                                  email=self.param['email'])
        dotrequest.save(force_insert=True)                          
        self.control = dotrequest.control #zapamiętujemy wygenerowany control
        self.req = RequestFactory()
        
    
        
        
    def _post(self,status,t_status,fake=False):
        control = self.control
        if fake:
            control += 'fake'
            
        md5 = generate_md5(control,self.param['t_id'],self.param['kwota'],self.param['email'],t_status)
        request = self.req.post('/dotpay/receiver/', {'id': DOTID,
                                     'status':status,
                                     'control':self.control,
                                     't_id':self.param['t_id'],
                                     'amount': self.param['kwota'],
                                     'orginal_amount': self.param['kwota'],
                                     't_status':t_status,
                                     'description':self.param['opis'],
                                     'md5':md5,
                                     't_date':datetime.now()})
        
        request.META['REMOTE_ADDR'] = DOTPAY_SERVERS[0]
        return request
    
    def testPostwithWrongIP(self):
        request = self._post(1,1)
        request.META['REMOTE_ADDR'] = '127.0.0.1'
        response = receiver(request) 
        self.assertEqual(response.status_code, 403,"CODE: "+str(response.status_code))
        
    def testResponses(self):
        for stat in STATUS_CHOICES:
            request = self._post(1,stat[0])
            response = receiver(request)  
            self.assertEqual(response.status_code, 200,"CODE: "+str(response.status_code)+" Typ: "+stat[1])
        self.assertEqual(len(DotResponse.objects.filter(control=self.control)),len(STATUS_CHOICES))
        
        global signal_count
        self.assertEqual(len(STATUS_CHOICES),signal_count)
        signal_count = 0
    
        
    
    def testFakeResponses(self):     
        for stat in STATUS_CHOICES:
            request = self._post(1,stat[0],True)
            response = receiver(request)  
            self.assertEqual(response.status_code, 500,"CODE: "+str(response.status_code)+" Typ: "+stat[1])

@dispatch.receiver(dot_anulowana)
@dispatch.receiver(dot_odmowa)
@dispatch.receiver(dot_nowa)        
@dispatch.receiver(dot_wykonana)
@dispatch.receiver(dot_reklamacja)
def signals(sender, **kwargs):
    global signal_count
    signal_count += 1

 