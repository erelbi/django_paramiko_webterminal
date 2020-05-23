from django.http import JsonResponse

import getpass
import subprocess
import os
from django.template.response import TemplateResponse
from django.views import View
from app.models import SSHconnect
import paramiko


class Register(View):
    def __init__(self):
        self.status = list()
        self.user = getpass.getuser()
        if self.user == 'root':
            self.ssh_dir = "/root/.ssh/"
        else:
            self.ssh_dir = "/home/%s/.ssh/" % (self.user)
        self.gen_key()
        self.host_know()
        self.ssh_connect = SSHconnect.objects.all()
        self.key = open(os.path.expanduser('~/.ssh/id_rsa.pub')).read()


    def get(self, request):
        table = self.client_status()
        response = TemplateResponse(request, 'index.html', {'table': table})
        return response

    def post(self, request):
        op = request.POST.get('op')
        print("if dışarda", op)
        if 'register' == op:
            try:
                host = request.POST.get('host')
                user = request.POST.get('user')
                port = request.POST.get('port')
                password = request.POST.get('password')
                print(host, user, port, password)
                SSHconnect.objects.create(ip=host, user=user, port=port)
                result = self.shhkeygen_send(host=host, user=user, port=port, password=password)
                return JsonResponse({"code": 200, 'data': result, 'ip': host, 'user': user})
            except Exception as err:
                return JsonResponse({"code": 500, 'data': err, 'ip': host, 'user': user})

    def host_know(self):
        if 'config' in os.listdir(self.ssh_dir):
            pass
        else:
            f = open("{}config".format(self.ssh_dir), "w")
            f.write("Host *  \n")
            f.write("StrictHostKeyChecking no \n")
            f.close
            return True

    def key_check(self):
        if 'id_rsa' in os.listdir(self.ssh_dir):
            return True
        else:
            return False

    def gen_key(self):
        if self.key_check():
            return True
        else:
            subprocess.call('ssh-keygen -t rsa -N "" -f id_rsa', shell=True, cwd=self.ssh_dir)
            return False

    def shhkeygen_send(self, host, user, port, password):
        print("ssh_keygen_send")
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(host, username=user, password=password, port=port)
            client.exec_command('mkdir -p ~/.ssh/')
            client.exec_command('echo "%s" >> ~/.ssh/authorized_keys' % self.key)
            client.exec_command('chmod 644 ~/.ssh/authorized_keys')
            client.exec_command('chmod 700 ~/.ssh/')
            client.exec_command(
                'if type restorecon >/dev/null 2>&1 ; then restorecon -F .ssh .ssh/authorized_keys ; fi')
            client.close()


        except Exception as err:
            print(err)
            return err

    def client_status(self):
        client_list = self.gen_list_client()
        try:
            print(client_list)
            for status_client in client_list:
                conn = paramiko.SSHClient()
                conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                print(status_client['ip'], status_client['user'], status_client['port'])
                #conn.connect(status_client['ip'], username=status_client['user'], port=status_client['port'],timeout=3, look_for_keys=False)
                conn.connect(status_client['ip'], username=status_client['user'], port=status_client['port'], timeout=3)

                SSHconnect.objects.filter(ip=status_client['ip']).update(status='online')
                if SSHconnect.objects.filter(ip=status_client['ip']).values('status') == None:
                    try:
                        os.popen(
                            'ssh -o StrictHostKeyChecking=no {}@{}'.format(status_client['user'], status_client['ip']),
                            shell=True)
                        SSHconnect.objects.filter(ip=status_client['ip']).update(status='online')

                    except:
                        SSHconnect.objects.filter(ip=status_client['ip']).update(status='offline')
                        continue
        except:
            SSHconnect.objects.filter(ip=status_client['ip']).update(status='offline')
            conn.close()
            pass

        return SSHconnect.objects.all()


    def gen_list_client(self):
        self.client_check = list()
        for client in self.ssh_connect:
            self.client_check.append(self.create_client_dict(client))
        return self.client_check

    def create_client_dict(self, client):
        self.client_dict = dict()
        self.client_dict['ip'] = client.ip
        self.client_dict['user'] = client.user
        self.client_dict['port'] = client.port
        return self.client_dict

