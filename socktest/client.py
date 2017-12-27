# -*- coding: utf-8 -*-
import sys
import socket
from socket import AF_UNIX

def main(argv):
    outsock = socket.socket(AF_UNIX)
    outsock.connect('/tmp/proxy_source.s')
    print(outsock.recv(1024))
    outsock.close()
    # pass


if __name__ == '__main__':
    sys.exit(main(sys.argv))
