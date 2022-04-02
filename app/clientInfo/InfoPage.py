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
import json
from django.core.files.storage import FileSystemStorage
from app.web_terminal.send_command import SSHclient
from django.core.files import File
from core.settings import BASHSCRIPT_DIR

class Infoclient(View):
    def __init__(self):
        self.system_info = BASHSCRIPT_DIR + ("system_info.sh",) #Neden tupple kullandık çünkü bize hem directory hem isim lazım... kıps :)

    def get(self,request,ip):
        get_system_info = Info.connection_bash_execute(file=self.system_info,ip=ip)
        get_disk_info = Info.connection_ssh_execute(command="lsblk --json",ip=ip)
        get_network_info = Info.connection_ssh_execute(command="ip --json address",ip=ip)
        get_systemctl = Info.connection_ssh_execute(command="systemctl list-units --type=service --state=active -o json",ip=ip)

        get_system_info_json = self.byte_to_json(get_system_info)
        get_system_disk_json = self.byte_to_json(get_disk_info)
        get_system_network_json = self.byte_to_json(get_network_info)
        get_systemctl_list_json = self.byte_to_json(get_systemctl)
        print(type(get_systemctl_list_json))


        return render(request, 'client/clientinfo.html',{'ip':ip,'client_info':get_system_info_json,
                                                         'client_disk_info':get_system_disk_json,
                                                         'system_network':get_system_network_json,
                                                         'systemctl': get_systemctl_list_json
                                                         } )
    def post(self, request,ip):
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        session = SSHclient.connc(ip)[0]
        sftp = SSHclient.connc(ip)[1].open_sftp()
        cd = os.path.realpath(MEDIA_URL)
        dd = ("{}".format(filename))
        sftp.put(dd, '/tmp/{}'.format(filename))

        return render(request,'clientinfo.html', { 'uploaded_file_url': uploaded_file_url,'ip':ip})

    def network_info(self):
        pass

    def pid_info(self,ip):
        command=" ps aux | awk -v OFS=, '{print $1, $2}' | jq"
        pid = (Info.connection_ssh_execute(ip, command)).decode('UTF-8')
        return pid

    def user_info(self):
        pass

    def system_info(self):
        pass

    def byte_to_json(self,output):
        try:
            return json.loads(output.decode('utf8'))
        except:
            raise


    def client_info(self,ip):


        try:
            command_ram = "free | grep Mem | awk '{print $3/$2 * 100.0}'"
            command_cpu = "NUMCPUS=`grep ^proc /proc/cpuinfo | wc -l`; FIRST=`cat /proc/stat | awk '/^cpu / {print $5}'`; sleep 1; SECOND=`cat /proc/stat | awk '/^cpu / {print $5}'`; USED=`echo 2 k 100 $SECOND $FIRST - $NUMCPUS / - p | dc`; echo ${USED} "
            command_disk = "df --output=pcent / | tr -dc '0-9'"

            ram = (Info.connection_ssh_execute(ip,command_ram)).decode('UTF-8')
            cpu = (Info.connection_ssh_execute(ip,command_cpu)).decode('UTF-8')
            disk = (Info.connection_ssh_execute(ip,command_disk)).decode('UTF-8')




            return  JsonResponse({'ram':ram.rsplit(',')[0],'cpu':cpu.rsplit(',')[0],'disk':disk})
        except Exception as err:
            print("ERROR {}".format(err))
            return client_info_dict

