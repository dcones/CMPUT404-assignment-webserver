#  coding: utf-8
import socketserver

# Copyright 2013 Daniel Cones
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
        if self.data and self.data[0] == 'GET':
            response = self.GET()
        else:
            response = "405 Method Not Allowed"
        response = "HTTP/1.1 "+response+"\r\n\r\n"
        return self.request.sendall(response.encode())

    def GET(self):
        if self.data[1].endswith("/"):
            self.data[1] += "index.html"

        try:
            if ".." in self.data[1]:
                raise FileNotFoundError
            prefix = "."
            if not self.data[1].startswith("/www"):
                prefix += "/www"
            with open(prefix+self.data[1], "r") as file:
                file_content = file.read()
        except IsADirectoryError:
            return "301 Moved Permanently\r\nLocation: {}".format(self.data[1]+"/")
        except FileNotFoundError:
            return "404 Not Found"
        except Exception as e:
            return "400 Bad Request"
        else:
            try:
                file_type = self.data[1].rsplit(".",1)[1]
            except:
                file_type = "plain"
            header = "200 OK\r\nContent-Type: text/{}\r\nContent-Length: {}".format(file_type,len(file_content))
            return header + "\r\n\r\n" + file_content

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)
    server.serve_forever()
