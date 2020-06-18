import paramiko

class ssh_conn:
    @classmethod
    def conn(cls,host,port,username,password):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=host,port=port,username=username,password=password)
        except Exception as e:
            print(f'{host}-ssh连接:{str(e)}')
            exit()
        else:
            return ssh

    @classmethod
    def cmd(cls,conn,shell,host,appname):
        stdin,stdout,stderr = conn.exec_command(shell)
        out,err = stdout.read().decode(),stderr.read().decode()
        if err:
            print(f'{host}--{appname}:{str(err)}')
        else:
            print(f"{host}--{appname}: 执行成功")

    @classmethod
    def cmd_echo(cls,conn,shell,host,appname):
        stdin,stdout,stderr = conn.exec_command(shell)
        out,err = stdout.readlines(),stderr.readlines()
        if err:
            err = "".join(err)
            print(f'{host}--{appname}:{str(err)}')
        else:
            for i in range(len(out)):
                out[i] = out[i].strip('\n')
            return out

    @classmethod
    def down(cls,conn):
        conn.close()
