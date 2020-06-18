import paramiko

class sftp_conn:
    @classmethod
    def conn(cls,host,port,username,password):
        try:
            sftp = paramiko.Transport(sock=(host,port))
            sftp.connect(username=username,password=password)
        except Exception as e:
            print(f'{host}-sftp连接:{str(e)}')
            exit()
        else:
            return sftp

    @classmethod
    def put_file(cls,sftp,localfile,remotefile):
        sftp_put = paramiko.SFTPClient.from_transport(sftp)
        sftp_put.put(localfile,remotefile)

    @classmethod
    def down(cls,sftp):
        sftp.close()

