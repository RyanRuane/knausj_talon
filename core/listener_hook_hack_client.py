#!/usr/bin/env python3
import socket
import sys

command_listener_host = ''
command_listener_port = 5000

if __name__ == "__main__":
    if len(sys.argv) > 1:
        msg = sys.argv[1].encode()
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((command_listener_host, command_listener_port))
            client_socket.send(msg)
        except Exception:
            client_socket.close()
