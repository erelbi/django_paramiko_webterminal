from app.models import BashScript
from django.http import JsonResponse

def ajax_delete(request,ip):
    if request.method == 'POST':
        name = request.POST.get('name')
        data = { 'is_delete': BashScript.objects.filter(name=name).delete()}
        return JsonResponse(data)

def ajax_update(request,ip):
    if request.method == 'POST':
        name = request.POST.get('name')
        point = request.POST.get('point')
        data= { 'is_update': BashScript.objects.filter(name=name).update(point=point)}
        return JsonResponse(data)
