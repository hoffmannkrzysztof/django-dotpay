# -*- encoding: utf-8 -*-
from django.conf import settings

DOTID = getattr(settings, 'DOTID', '49740')
DOTPIN = getattr(settings, 'DOTPIN', '4564567567456')
DOTURL  = getattr(settings, 'DOTURL ', 'http://localhost:8000/thankyou')
DOTURLC  = getattr(settings, 'DOTURLC', 'http://localhost:8000/dotpay/recevier/')
DOTTXTGUZIK  = getattr(settings, 'DOTTXTGUZIK', 'Powrót do sklepu')
DOTORDERMODEL = getattr(settings, 'DOTORDERMODEL', None)
