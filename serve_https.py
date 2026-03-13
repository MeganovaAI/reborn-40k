import http.server
import ssl
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

server = http.server.HTTPServer(('0.0.0.0', 8443), http.server.SimpleHTTPRequestHandler)
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain('cert.pem', 'key.pem')
server.socket = ctx.wrap_socket(server.socket, server_side=True)

print(f'Serving HTTPS on https://40.49.6.2:8443/')
print(f'  Demo: https://40.49.6.2:8443/demo.html')
print(f'  (Accept the self-signed cert warning in your browser)')
server.serve_forever()
