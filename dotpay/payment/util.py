# -*- coding: utf-8 -*-
import hashlib
from dotpay.settings import DOTID
from dotpay.payment.settings import DOTPIN

TRANS_STATUS_CHOICES = (
('OK','OK'),
('FAIL','FAIL')   
)


STATUS_CHOICES = (
('1','NOWA'),
('2','WYKONANA'),
('3','ODMOWA'),
('4','ANULOWANA/ZWROT'),
('5','REKLAMACJA'),                                     
)

DOTPAY_SERVERS = ['195.150.9.37']


def generate_md5(control,t_id,amount,t_status, email):
    list = []
    #PIN:id:control:t_id:amount:email:service:code:username:password:t_status
    
    list.append(DOTPIN)
    list.append(DOTID)
    list.append(control)
    list.append(t_id)
    list.append(amount)
    list.append(email) #email
    list.append("") #service
    list.append("") #code
    list.append("") #username
    list.append("") #password
    list.append(t_status)
    
    list = map(lambda o: str(o), list)
    
    return hashlib.md5(":".join(list)).hexdigest()
