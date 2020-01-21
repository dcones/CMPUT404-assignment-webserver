#  coding: utf-8
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).decode().strip().split()
        if self.data[0] != 'GET':
            return self.request.sendall(bytearray("405 Method Not Allowed", "utf-8"))
        self.GET()

    def GET(self):
        if not self.data[1].startswith("/www/"):
            return self.request.sendall(bytearray("403 Forbidden", "utf-8"))
        try:
            # import pdb;pdb.set_trace()
            with open("."+self.data[1], "rb") as file:
                file_content = file.read()
                message = """HTTP/1.1 200 OK\r
                            Content-Type: text/html\r
                            Content-Length: {}\r
                            \r\n""".format(len(file_content)).encode()
                self.request.sendall(message)
                self.request.sendall(file_content)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
