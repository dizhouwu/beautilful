import logging
import datetime
from paramiko import SFTPClient, Transport
from contextlib import contextmanager


class SFTPClient:
    def __init__(self, *, host='', password='', username='', port=22):
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
