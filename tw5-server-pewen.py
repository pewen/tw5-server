#!/usr/bin/python3
# by FNB
#
import os
import argparse
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, HTTPServer


class TiddlyWiki5Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)

    def do_PUT(self):
        with open(os.path.join(self.directory, self.path[1:]), 'wb') as fp:
            bytes_remaining = int(self.headers['content-length'])
            while bytes_remaining > 0:
                bytes_remaining -= fp.write(self.rfile.read1())
        self.send_response(HTTPStatus.OK)
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(HTTPStatus.OK)
        self.send_header('DAV', 'tw5/put')
        self.end_headers()


def run(
    server=HTTPServer, handler=TiddlyWiki5Handler, addr="localhost", port=8000
):
    server_address = (addr, port)
    httpd = server(server_address, handler)

    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Simple Tiddly Wiki 5 server")
    parser.add_argument(
        "-l",
        "--listen",
        default="localhost",
        help="Specify the IP address on which the server listens",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8000,
        help="Specify the port on which the server listens",
    )
    args = parser.parse_args()
    run(addr=args.listen, port=args.port)
