#!/usr/bin/env python3
"""Simple HTTPS server for REBORN 40K (camera mode requires HTTPS).
Auto-generates a self-signed cert if cert.pem/key.pem are missing."""

import http.server
import ssl
import os
import subprocess

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Auto-generate self-signed cert if missing
if not os.path.exists('cert.pem') or not os.path.exists('key.pem'):
    print('Generating self-signed SSL certificate...')
    subprocess.run([
        'openssl', 'req', '-x509', '-newkey', 'rsa:2048',
        '-keyout', 'key.pem', '-out', 'cert.pem',
        '-days', '365', '-nodes',
        '-subj', '/CN=localhost',
    ], check=True)
    print('Created cert.pem and key.pem')

server = http.server.HTTPServer(('0.0.0.0', 8443), http.server.SimpleHTTPRequestHandler)
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain('cert.pem', 'key.pem')
server.socket = ctx.wrap_socket(server.socket, server_side=True)

print(f'\nServing HTTPS on https://localhost:8443/')
print(f'  Open: https://localhost:8443/index.html')
print(f'  (Accept the self-signed cert warning in your browser)')
server.serve_forever()
