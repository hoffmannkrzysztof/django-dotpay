from django.shortcuts import render_to_response
from django.template.context import RequestContext
from dotpay.sms.forms import DotSMSCheckForm

def form(request):
    price = ""
    if request.POST:
        form = DotSMSCheckForm(request.POST)
        if form.is_valid(): #sms code is valid and ready to use
            form.save()
            price = form.instance.value # value of sms returned from dotpay
    else:
        form = DotSMSCheckForm()
    return render_to_response('form-sms.html',{'form':form,'price':price},context_instance=RequestContext(request))