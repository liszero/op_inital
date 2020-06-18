from pexpect import pxssh

class ppt:
    def __init__(self,host,username,password,port):
        self.host = host
        self.username = username
        self.password = password
        self.port = port

    def ppt_conn(self):
        try:
            s = pxssh.pxssh()
            s.login(server=self.host,username=self.username,password=self.password,port=self.port)
        except Exception as e:
            print(f'{self.host}-ssh连接:{str(e)}')
            exit()
        else:
            return s

    def ppt_action(self,client,cmd_list,host,appname):
        for i in cmd_list:
            client.sendline(i)
            client.prompt()
        print(f'{host}--{appname}:{client.before.decode()}')

    def ppt_close(self,client):
        client.logout()