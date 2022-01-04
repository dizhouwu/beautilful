import os
from paramiko import SFTPClient, Transport
from contextlib import contextmanager

from stat import S_ISDIR, S_ISREG    

def sftp_get_recursive(path, dest, sftp):
    item_list = sftp.listdir_attr(path)
    dest = str(dest)
    if not os.path.isdir(dest):
        os.makedirs(dest, exist_ok=True)
    for item in item_list:
        mode = item.st_mode
        if S_ISDIR(mode):
            sftp_get_recursive(path + "/" + item.filename, dest + "/" + item.filename, sftp)
        else:
            sftp.get(path + "/" + item.filename, dest + "/" + item.filename)
            
class SSHFTPClient:
    def __init__(self, *, host="", password="", username="", port=22):
        self.host = host
        self.port = port
        self.password = password
        self.username = username

    @contextmanager
    def yield_conn(self):
        transport = Transport(sock=(self.host, self.port))
        transport.connect(username=self.username, password=self.password)
        conn = SFTPClient.from_transport(transport)
        try:
            yield conn
        finally:
            conn.close()

    def get_conn(self):
        transport = Transport(sock=(self.host, self.port))
        transport.connect(username=self.username, password=self.password)
        conn = SFTPClient.from_transport(transport)
        return conn

# SSH Client
import paramiko
ssh = paramiko.SSHClient()
from paramiko.rsakey import RSAKey

ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
pkey = paramiko.RSAKey.from_private_key_file("host_keys-cert.pub")
ssh.connect(host,username=username,pkey=pkey)
sftp = ssh.open_sftp()
sftp.listdir()
