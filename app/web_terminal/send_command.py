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
from app.clientInfo.clientinfo import Info



class SSHclient(View):
    def __init__(self):
        self.script = BashScript.objects.all()

    def get(self,request,ip):
        form=BashScriptForm()
        return render(request, 'client/sendcommand.html',{'ip':ip,'form':form,'db':self.script} )
    def post(self, request,ip):
        user = request.user.username
        form = BashScriptForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author=user
            form.save()
            return HttpResponseRedirect(reverse('client_command',args=(ip,)))
        else:
                form = BashScriptForm()
                return render(request,'client/sendcommand.html', {'form':form,'db':self.script})

    @staticmethod
    def connc(ip):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        user = SSHconnect.objects.filter(ip=ip).first().user
        port = SSHconnect.objects.filter(ip=ip).first().port
        ssh.connect(ip, username=user, port=port)
        transport = ssh.get_transport()
        session = transport.open_session()
        session.set_combine_stderr(True)
        session.get_pty()
        return session,ssh



    def run(self,command,ip):
        session= SSHclient.connc(ip)[0]
        session.exec_command(command)
        stdout = session.makefile('r', -1)
        for line in iter(stdout.readline, ""):
            yield line
        session.close()


    def bashscript(self,bash_script,ip):
        session = SSHclient.connc(ip)[0]
        sftp = SSHclient.connc(ip)[1].open_sftp()
        cd = os.path.realpath(MEDIA_URL)
        file = '{}'.format(bash_script)
        dd = (cd+"/"+file )
        sftp.put(dd, '/opt/djangobashscript.sh')

        session.exec_command('cd /opt; chmod 0755 djangobashscript.sh; bash djangobashscript.sh')
        stdout = session.makefile('r', -1)
        for line in iter(stdout.readline, ""):
            yield line
        sftp.close()
        session.close()

    def stream(self,ip,command,*args,**kwargs):
        script = BashScript.objects.values_list('name',  flat=True)
        if  str(command) in script:
            stream = SSHclient.bashscript(self,command,ip)

        else:
            stream = SSHclient.run(self,command,ip)

        response = StreamingHttpResponse(stream, status=200, content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        return response






