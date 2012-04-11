# coding=utf-8

from django.shortcuts import render_to_response
from django.template.context import RequestContext

from dotpay.payment.models import DotRequest
from dotpay.payment.forms import DotRequestForm
from order.models import Order
from django.views.decorators.cache import cache_control

@cache_control( no_store=True,no_cache=True,must_revalidate=True,post_check=0,pre_check=0, max_age=0 )
def form(request):
    dotrequest = DotRequest.objects.create(kwota=24.99,opis='Testowe zamówienie',email='adres@email.pl')
    Order.objects.create(request=dotrequest,user_id=1 )
    form = DotRequestForm(instance=dotrequest)
    return render_to_response('form.html',{'form':form},context_instance=RequestContext(request))



