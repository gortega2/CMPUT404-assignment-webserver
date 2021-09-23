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
http_code_dict = {200:"OK", 404:"File Not Found", 405:"Method Not Allowed"}
#print(CWD)
class MyWebServer(socketserver.BaseRequestHandler):
    

    def parse_request(self, msg):
        split_msg = msg.split("\r\n")
        print(split_msg)
        if 'GET' in split_msg[0]:
            url = split_msg[0].split()[1]
            print("Printing URL")
            print(url)
            print(parse.urlparse(url))
            print("THE MIME TYPE OF THE URL IS: {}".format(mimetypes.guess_type(url)))
            mime_type = mimetypes.guess_type(url)
            test = self.do_GET(url)
            if test != None:
                self.send_message(200, mime_type,msg=test)
                return
            else:
                self.send_message(404)

        else:
            print("send error code")
            self.do_GET(405)



        return

    def send_message(self, code, type='', msg=''):
        print(self.send_http_headers(code, type, msg))
        self.request.sendall(bytearray(self.send_http_headers(code, type, msg), FORMAT))
        '''
        if code == 405:
            data = "HTTP/1.1 405 Method Not Allowed\r\n"
            data += "Connection: close\r\n\r\n"
            self.request.sendall(bytearray(data, FORMAT))
        elif code == 200:
            data = "HTTP/1.1 200 OK\r\n"
            data += 'Content-Type: text/html\r\n'
            data += 'Connection: close \r\n\r\n'
            data += str(msg)
            
            self.request.sendall(bytearray(data, FORMAT))
        
        elif code == 404:
            data = 'HTTP/1.1 404 File Not Found'
            data += "Connection: close \r\n\r\n"
            self.request.sendall(bytearray(data, FORMAT))
        '''

        return

    def send_http_headers(self, code, type, msg):
        data = "HTTP/1.1 {} {}\r\n".format(code, http_code_dict[code])
        data += "Date: {}\r\n".format(formatdate(timeval=None, localtime=False, usegmt=True))
        if code >= 200 and code < 300:
            data += 'Content-Type: {}\r\n'.format(type[0])
            data += 'Connection: close\r\n\r\n'
            data += str(msg)
            return data
        elif code >=400 and code < 500:
            data += 'Connection: close\r\n\r\n'
            return data
        else:
            return
        

    def do_GET(self, request):
        if request == '/':

            #with open('www/base.css', 'r') as f:
                #data = f.read()

            #TODO: FIX THE PATH AS IT WILL NOT WORK ON LAB MACHINES, ONLY ON THIS MACHINE!!!!!!!!!!!!
            with open('www/index.html' ,'r') as f:
                data = f.read()
        
            print(data)
            return data

        else:
            path = CWD + request
            print("PRINTING REQUEST: ", request)
            #checks if the path is valid
            if "/../" not in request:           # Lazy fix
            #TODO: PROPERLY IMPLEMENT CHECKING IF THE REQUEST PATH IS IN /WWW/ DIR
            #if Path(CWD) in Path(path).parents:
                if os.path.exists(path):
                    #TODO: CHECK IF THE PAHT IS A DIR
                    with open(CWD+request, 'r') as f:
                        data = f.read()
                    return data
                else:
                    return
            else:
                print("PATH CHECK ELSE STATEMENT")
                return
        return


    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        '''
        data = "HTTP/1.1 200 OK\r\n"
        data += "TESTING \r\n"
        data += "Connection: close \r\n\r\n"
        '''
        #self.request.sendall(bytearray("HTTP/1.1 200 OK",'utf-8'))
        #self.request.sendall(bytearray("TESTING", FORMAT))
        #self.request.sendall(bytearray(data, FORMAT))
        print("UTF decode: ",self.data.decode(FORMAT))
        #print("Attempting to print path")
        #print(parse.urlparse(self.data.decode(FORMAT)).port)
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
