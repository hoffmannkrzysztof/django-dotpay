# -*- coding: utf-8 -*-

from django import test
from dotpay.payment.models import DotResponse, DotRequest
from dotpay.settings import DOTID
from datetime import datetime
from django.test.client import RequestFactory

from dotpay.payment.util import generate_md5, STATUS_CHOICES, DOTPAY_SERVERS
from dotpay.payment.views import receiver
from dotpay.payment.signals import dot_wykonana, dot_anulowana, dot_odmowa, dot_nowa, \
    dot_reklamacja
from django import dispatch
from django.core.urlresolvers import reverse

signal_count = 0


class DotPayTest(test.TestCase):
    def create_request(self):
        self.param = {}
        self.param['kwota'] = str(24.33)
        self.param['opis'] = 'Testowe zamówienie #1'
        self.param['email'] = 'krzysiekpl@gmail.com'
        self.param['t_id'] = 'TST-20102'

        dotrequest = DotRequest(kwota=self.param['kwota'],
                                  opis=self.param['opis'],
                                  email=self.param['email'])
        dotrequest.save(force_insert=True)
        self.control = dotrequest.control #zapamiętujemy wygenerowany control
        self.request = dotrequest
    def setUp(self):
        self.req = RequestFactory()




    def _post(self, status, t_status, fake=False, user_changed_email=False):
        self.create_request()
        control = self.control
        if fake:
            control += 'fake'


        if user_changed_email:
            email = 'sfdjkgfk@gf.pl'
        else:
            email = self.param['email']

        md5 = generate_md5(control, self.param['t_id'], self.param['kwota'], t_status, email)
        request = self.req.post(reverse('dotpay_receiver'), {'id': DOTID,
                                     'status':status,
                                     'control':self.control,
                                     't_id':self.param['t_id'],
                                     'amount': self.param['kwota'],
                                     'orginal_amount': self.param['kwota'],
                                     'email': email,
                                     't_status':t_status,
                                     'description':self.param['opis'],
                                     'md5':md5,
                                     't_date':datetime.now()})

        request.META['REMOTE_ADDR'] = DOTPAY_SERVERS[0]
        return request

    def testPostwithWrongIP(self):
        request = self._post(1, 1)
        request.META['REMOTE_ADDR'] = '127.0.0.1'
        response = receiver(request)
        self.assertEqual(response.status_code, 403, "CODE: " + str(response.status_code))

    def testResponses(self):
        for stat in STATUS_CHOICES:
            request = self._post(1, stat[0])
            response = receiver(request)
            self.assertEqual(response.status_code, 200, "CODE: " + str(response.status_code) + " Typ: " + stat[1])
        self.assertEqual(DotResponse.objects.count(), len(STATUS_CHOICES))

        global signal_count
        self.assertEqual(len(STATUS_CHOICES), signal_count)
        signal_count = 0


    def testResponseswithchangedemail(self):
        for stat in STATUS_CHOICES:
            request = self._post(1, stat[0], False, True)
            response = receiver(request)
            self.assertEqual(response.status_code, 200, "CODE: " + str(response.status_code) + " Typ: " + stat[1])
        self.assertEqual(DotResponse.objects.count(), len(STATUS_CHOICES))

        global signal_count
        self.assertEqual(len(STATUS_CHOICES), signal_count)
        signal_count = 0



    def testFakeResponses(self):
        for stat in STATUS_CHOICES:
            request = self._post(1, stat[0], True)
            response = receiver(request)
            self.assertEqual(response.status_code, 500, "CODE: " + str(response.status_code) + " Typ: " + stat[1])

    def testMultipleResponseToSingleRequest(self):
        request = self._post(1, 1)
        response = receiver(request)
        self.assertEqual(response.status_code, 200, "First transaction should success.")
        self.assertEqual(DotResponse.objects.count(), 1)
        response = receiver(request)
        self.assertEqual(response.status_code, 200, "Second transaction should success.")
        self.assertEqual(DotResponse.objects.count(), 1, "Secent transaction should not create response.")

        global signal_count
        self.assertEqual(1, signal_count)
        signal_count = 0

@dispatch.receiver(dot_anulowana)
@dispatch.receiver(dot_odmowa)
@dispatch.receiver(dot_nowa)
@dispatch.receiver(dot_wykonana)
@dispatch.receiver(dot_reklamacja)
def signals(sender, **kwargs):
    global signal_count
    signal_count += 1


