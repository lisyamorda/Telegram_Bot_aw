# -*- coding: utf-8 -*-
import os
import sys
import socket
import io


def main(argv):
    if os.path.exists("/tmp/proxy_source.s"):
        os.remove("/tmp/proxy_source.s")
        # os.
    insock = socket.socket(socket.AF_UNIX)
    # outsock = socket.socket(socket.AF_UNIX)
    insock.bind('/tmp/proxy_source.s')
    insock.listen()
    # while True:
    outsock, addr = insock.accept()
    outsock.send(b'HelloWorld')
    insock.close()
    # wrap = io.TextIOWrapper()
    # wrap.readline()
    # wrap.write('hello world')
    pass


if __name__ == '__main__':
    sys.exit(main(sys.argv))
