from django.views.decorators.csrf import csrf_exempt
from dotpay.models import DotResponse
from django.http import HttpResponse
from dotpay.util import DOTPAY_SERVERS

@csrf_exempt    
def receiver(request):
    if request.POST:
        if request.META['REMOTE_ADDR'] in DOTPAY_SERVERS:
            vars= {}
            for field in DotResponse._meta.fields:
                if field.name != 'request':
                    vars[field.name] = request.POST.get(field.name,None)
            try:
                dotresponse = DotResponse(**vars)
                dotresponse.save()
            except:
                return HttpResponse("ERR",status=500)
            else:
                return HttpResponse("OK",status=200)
        else:
            return HttpResponse("ERR",status=403)
    else:
        return HttpResponse("405 Method Not Allowed",status=405)