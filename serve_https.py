#!/usr/bin/env python3
"""REBORN 40K server with HTTPS + asset upload API.
Auto-generates a self-signed cert if cert.pem/key.pem are missing."""

import http.server
import ssl
import os
import subprocess
import json
import base64
import uuid
import socket

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.makedirs('uploads', exist_ok=True)

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


def get_local_ip():
    """Get the machine's LAN IP for QR codes."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return 'localhost'


HOST_IP = get_local_ip()
PORT = 8443


class Reborn40kHandler(http.server.SimpleHTTPRequestHandler):
    """Serves static files + handles POST /api/upload for asset sharing."""

    def do_POST(self):
        if self.path == '/api/upload':
            self.handle_upload()
        else:
            self.send_error(404, 'Not found')

    def handle_upload(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            data = json.loads(body)

            asset_id = uuid.uuid4().hex[:10]
            result = {'id': asset_id, 'assets': {}}

            # Save card image
            if data.get('card_image'):
                b64 = data['card_image']
                # Strip data URL prefix if present
                if ',' in b64:
                    b64 = b64.split(',', 1)[1]
                img_bytes = base64.b64decode(b64)
                fname = f'{asset_id}_card.jpg'
                with open(f'uploads/{fname}', 'wb') as f:
                    f.write(img_bytes)
                result['assets']['card_url'] = f'https://{HOST_IP}:{PORT}/uploads/{fname}'

            # Save video URL reference (video is already hosted remotely)
            if data.get('video_url'):
                result['assets']['video_url'] = data['video_url']

            # Save character name/faction for the share page
            meta = {
                'name': data.get('name', 'Unknown'),
                'faction': data.get('faction', ''),
                'card_url': result['assets'].get('card_url', ''),
                'video_url': result['assets'].get('video_url', ''),
            }
            with open(f'uploads/{asset_id}.json', 'w') as f:
                json.dump(meta, f)

            # Build share page URL
            result['share_url'] = f'https://{HOST_IP}:{PORT}/share.html?id={asset_id}'

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def do_OPTIONS(self):
        """Handle CORS preflight."""
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()


server = http.server.HTTPServer(('0.0.0.0', PORT), Reborn40kHandler)
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain('cert.pem', 'key.pem')
server.socket = ctx.wrap_socket(server.socket, server_side=True)

print(f'\nREBORN 40K Server')
print(f'  Demo:    https://{HOST_IP}:{PORT}/index.html')
print(f'  Upload:  POST https://{HOST_IP}:{PORT}/api/upload')
print(f'  Uploads: https://{HOST_IP}:{PORT}/uploads/')
print(f'  (Accept the self-signed cert warning in your browser)')
server.serve_forever()
