import paramiko
import os
from app.models import BashScript
from django.http import JsonResponse


def script(request,ip):
        id = request.POST.get('id')
        op = request.POST.get('op')
        if op == "delete":
            try:
                BashScript.objects.filter(id=id).delete()
                return JsonResponse({'data': '{}.id Delete BashScript'.format(id)})
            except Exception as err:
                return JsonResponse({'data': err})


        elif op == "run":
            try:
                name = BashScript.objects.filter(id=id).values('name').first()
                script = BashScript.objects.filter(id=id).values('script').first()
                file =open(os.path.join(MEDIA_URL, '{}'.format(name['name'])), 'w')
                file.write(script['script'])
                file.close()
                return JsonResponse({'data': "Add To Script"})
            except Exception as err:
                return JsonResponse({'data': err})
