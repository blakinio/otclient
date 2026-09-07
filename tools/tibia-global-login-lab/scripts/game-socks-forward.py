#!/usr/bin/env python3
import json
import select
import socket
import struct
import threading
from pathlib import Path

HANDOFF = Path('/lab/secrets/login-handoff.json')
READY = Path('/lab/runtime/game-socks-forward.ready')
GRANTED = Path('/lab/runtime/game-socks-forward.granted')
CLIENT_BYTES = Path('/lab/runtime/game-socks-forward.client-bytes')
SERVER_BYTES = Path('/lab/runtime/game-socks-forward.server-bytes')
CLIENT_LENGTH = Path('/lab/runtime/game-socks-forward.client-length')
SERVER_LENGTH = Path('/lab/runtime/game-socks-forward.server-length')
LISTEN_HOST = '127.0.0.1'
LISTEN_PORT = 37171
SOCKS_HOST = '127.0.0.1'
SOCKS_PORT = 25344


def recv_exact(sock, size):
    data = bytearray()
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            raise ConnectionError('unexpected EOF')
        data.extend(chunk)
    return bytes(data)


def connect_via_socks(target_host, target_port):
    upstream = socket.create_connection((SOCKS_HOST, SOCKS_PORT), timeout=15)
    upstream.sendall(b'\x05\x01\x00')
    if recv_exact(upstream, 2) != b'\x05\x00':
        raise ConnectionError('SOCKS authentication negotiation failed')

    host = target_host.encode('idna')
    if not host or len(host) > 255:
        raise ValueError('invalid target host length')
    upstream.sendall(b'\x05\x01\x00\x03' + bytes([len(host)]) + host + struct.pack('!H', target_port))

    header = recv_exact(upstream, 4)
    if header[0] != 5 or header[1] != 0:
        raise ConnectionError('SOCKS connect request rejected')
    if header[3] == 1:
        recv_exact(upstream, 4)
    elif header[3] == 3:
        recv_exact(upstream, recv_exact(upstream, 1)[0])
    elif header[3] == 4:
        recv_exact(upstream, 16)
    else:
        raise ConnectionError('invalid SOCKS address type')
    recv_exact(upstream, 2)
    upstream.settimeout(None)
    GRANTED.touch(mode=0o600, exist_ok=True)
    return upstream


def relay(client, target_host, target_port):
    upstream = None
    client_length = 0
    server_length = 0
    try:
        upstream = connect_via_socks(target_host, target_port)
        sockets = [client, upstream]
        while True:
            readable, _, _ = select.select(sockets, [], [], 30)
            if not readable:
                continue
            for source in readable:
                data = source.recv(65536)
                if not data:
                    return
                if source is client:
                    client_length += len(data)
                    CLIENT_BYTES.touch(mode=0o600, exist_ok=True)
                    CLIENT_LENGTH.write_text(str(client_length), encoding='ascii')
                else:
                    server_length += len(data)
                    SERVER_BYTES.touch(mode=0o600, exist_ok=True)
                    SERVER_LENGTH.write_text(str(server_length), encoding='ascii')
                (upstream if source is client else client).sendall(data)
    except (OSError, ValueError):
        return
    finally:
        client.close()
        if upstream is not None:
            upstream.close()


def main():
    handoff = json.loads(HANDOFF.read_text(encoding='utf-8'))
    target_host = handoff['worldHost']
    target_port = int(handoff['worldPort'])

    READY.unlink(missing_ok=True)
    GRANTED.unlink(missing_ok=True)
    CLIENT_BYTES.unlink(missing_ok=True)
    SERVER_BYTES.unlink(missing_ok=True)
    CLIENT_LENGTH.unlink(missing_ok=True)
    SERVER_LENGTH.unlink(missing_ok=True)
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind((LISTEN_HOST, LISTEN_PORT))
    listener.listen(4)
    READY.touch(mode=0o600)

    while True:
        client, _ = listener.accept()
        threading.Thread(target=relay, args=(client, target_host, target_port), daemon=True).start()


if __name__ == '__main__':
    main()
