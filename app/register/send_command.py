import paramiko
import os
from core.settings import MEDIA_URL
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, StreamingHttpResponse
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views import View
from app.models import SSHconnect
from app.forms import BashScriptForm
from app.models import BashScript


class SSHclient(View):
    def __init__(self):
        self.script = BashScript.objects.all()

    def get(self,request,ip):
        form=BashScriptForm()
        return render(request, 'sendcommand.html',{'ip':ip,'form':form,'db':self.script} )
    def post(self, request,ip):
        user = request.user.username
        form = BashScriptForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author=user
            form.save()
            return (HttpResponseRedirect(reverse('client_command',args=(ip,))))
        else:
                form = BashScriptForm()
                return render(request,'sendcommand.html', {'form':form,'db':self.script})



    def run(self,command,ip):
        self.user = SSHconnect.objects.filter(ip=ip).first().user
        self.port = SSHconnect.objects.filter(ip=ip).first().port
        self.ip = ip
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip, username=self.user, port=self.port)
        transport = ssh.get_transport()
        session = transport.open_session()
        session.set_combine_stderr(True)
        session.get_pty()
        session.exec_command(command)
        stdout = session.makefile('r', -1)
        for line in iter(stdout.readline, ""):
            yield line
        ssh.close()


    def bashscript(self,bash_script,ip):
        print(bash_script,ip)
        user = SSHconnect.objects.filter(ip=ip).first().user
        port = SSHconnect.objects.filter(ip=ip).first().port
        ip = ip
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=user, port=port)
        sftp = ssh.open_sftp()
        transport = ssh.get_transport()
        session = transport.open_session()
        session.set_combine_stderr(True)
        session.get_pty()
        cd = os.path.realpath(MEDIA_URL)
        file = '{}'.format(bash_script)
        dd = (cd+"/"+file )
        sftp.put(dd, '/opt/djangobashscript.sh')
        # sftp.chmod('/opt/c.sh', 2777)
        session.exec_command('cd /opt; chmod 0755 djangobashscript.sh; bash djangobashscript.sh')
        stdout = session.makefile('r', -1)
        for line in iter(stdout.readline, ""):
            yield line
        sftp.close()
        ssh.close()









    def stream(self,ip,command,*args,**kwargs):
        script = BashScript.objects.values_list('name',  flat=True)
        if  str(command) in script:
            stream = SSHclient.bashscript(self,command,ip)

        else:
            stream = SSHclient.run(self,command,ip)

        response = StreamingHttpResponse(stream, status=200, content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        return response

def post_ajax(request, ip):
    if request.is_ajax():
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
                file=open(os.path.join(MEDIA_URL, '{}'.format(name['name'])), 'w')
                file.write(script['script'])
                file.close()
                return JsonResponse({'data': "Add To Script"})
            except Exception as err:
                return JsonResponse({'data': err})
