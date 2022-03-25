import paramiko
import os
from app.models import SSHconnect

class Info:

    @staticmethod
    def find_user_and_port(ip):
        try:
            user = SSHconnect.objects.filter(ip=ip).first().user
            port = SSHconnect.objects.filter(ip=ip).first().port
            return user,port
        except:
            raise

    @staticmethod
    def connection_ssh_execute(ip ,command):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            user,port = Info.find_user_and_port(ip)
            ssh.connect(ip, username=user, port=port)
            (stdin, stdout, stderr) = ssh.exec_command(command)
            cmd_output = stdout.read()
            ssh.close()
            return cmd_output
        except Exception as err:
            ssh.close()
            print("Error  connection_ssh_execute{}".format(err))
            return None

    @staticmethod
    def connection_bash_execute(file,ip):
        #file tupple  gelecek
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            user, port = Info.find_user_and_port(ip)
            ssh.connect(ip, username=user, port=port)
            sftp = ssh.open_sftp()
            print(file[0],file[1])
            sftp.put("{}/{}".format(file[0],file[1]), '/tmp/{}'.format(file[1]))
            (stdin, stdout, stderr) = ssh.exec_command('cd /tmp; chmod 0755 {}; bash {}'.format(file[1],file[1]))
            cmd_output = stdout.read()
            ssh.close()
            return cmd_output
        except:
            raise

