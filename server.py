#  coding: utf-8 
import socketserver
from urllib import parse
from pathlib import Path
import os
from email.utils import formatdate
import mimetypes
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

#HEADER = 64
FORMAT = 'utf-8'

CWD = str(Path.cwd()) + '/www'
mime_dict = {'.css':'text/css', '.html':'text/html'}
http_code_dict = {200:"OK", 301:"Moved Permanently", 404:"Not Found", 405:"Method Not Allowed"}
#print(CWD)
class MyWebServer(socketserver.BaseRequestHandler):
    

    def parse_request(self, msg):
        split_msg = msg.split("\r\n")
        if 'GET' in split_msg[0]:
            url = split_msg[0].split()[1]
            mime_type = mimetypes.guess_type(url)
            code, new_url = self.test_url(url)
            print('new url: %s' % (new_url))
            self.send_message(code, new_url)
        else:
            self.send_message(405, None)
            '''
            print(self.test_url(url))
            if test != None:
                self.send_message(200, mime_type,msg=test)
                return
            elif test == 301:
                self.send_message(301, msg=url)
            else:
                self.send_message(404)

        else:
            print("send error code")
            self.send_message(405)
            '''



        return

    def send_message(self, code, url):
        #rint(self.send_http_headers(code, type, msg))
        #self.request.sendall(bytearray(self.send_http_headers(code, type, msg), FORMAT))
        mess_send = self.send_http_headers(code, url)
        test = mess_send.split('\r\n')
        for x in test:
            print(x)
            if 'Connection: close' in x:
                break
        print('\n')
        self.request.sendall(bytearray(mess_send, FORMAT))
        return

    #Takes in the url the user is requesting and returns an http code depending on if it;s correct
    def test_url(self, url):
        path = CWD + url
        print("test path url: ", path)
        if url == '/': # THis if statement can probably be deleted later
            return 200, path + 'index.html'
        elif '/../' in path:
            return 404, None
        else:
            if os.path.exists(path):
                if os.path.isdir(path):
                    if path.endswith('/'):
                        return 200, path + 'index.html'
                    else:
                        return 301, url + '/'
                else:
                    return 200, path
            else:
                return 404, None
        return
    def send_http_headers(self, code, url):
        data = "HTTP/1.1 {} {}\r\n".format(code, http_code_dict[code])
        data += "Date: {}\r\n".format(formatdate(timeval=None, localtime=False, usegmt=True))
        if url != None:
            type = mimetypes.guess_type(url)
        if code >= 200 and code < 300:
            data += 'Content-Type: {}\r\n'.format(type[0])
            message_body = self.get_data(url, type[0])
            if 'html' in type[0] or 'css' in type[0]:
                data += 'Content-Length: {}\r\n'.format(len(message_body.encode(FORMAT)))
            else:
                data += 'Content-Length: {}\r\n'.format(len(message_body))
            data += 'Connection: close\r\n\r\n'
            data += str(message_body)
            return data
        elif code == 301:
            data += "Location: {}\r\n".format(url)
            data += "Connection: close\r\n\r\n"
            print(data)
            return data

        elif code >=400 and code < 500:
            data += 'Connection: close\r\n\r\n'
            return data
        else:
            return
        
    def get_data(self, path, type):
        if 'html' in type or 'css' in type:
            with open(path, 'r') as f:
                data = f.read()
                f.close()
        else:
            with open(path, 'rb') as f:
                data = f.read()
                f.close()
        return data

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        self.parse_request(self.data.decode(FORMAT))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080
    #print(formatdate(timeval=None, localtime=False, usegmt=True))
    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
