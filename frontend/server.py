#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
import requests
import re

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        
        if None != re.search('/*', self.path):
            self._set_response()
            try:
                response = requests.get(url='http://backend1:8080')
                backend1 = json.loads(response.text)
                backend1_name = backend1["name"]
                backend1_version = backend1["version"]
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                backend1_name = "backend1"
                backend1_version = "unavailable"

            try:
                response = requests.get(url='http://backend2:8080')
                backend2 = json.loads(response.text)
                backend2_name = backend2["name"]
                backend2_version = backend2["version"]
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                backend2_name = "backend2"
                backend2_version = "unavailable"

            name = "frontend"
            version = "1"
            message = f"<table><tr><td>Service</td><td>Version</td></tr><tr><td>{name}</td><td>{version}</td></tr><tr><td>{backend1_name}</td><td>{backend1_version}</td></tr><tr><td>{backend2_name}</td><td>{backend2_version}</td></tr></table>"

            content = f"<html><body><h1>{message}</h1></body></html>"
            self.wfile.write(content.encode(encoding='utf_8'))
            return

def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting server...\n')

    # start listening 
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()