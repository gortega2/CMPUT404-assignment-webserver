#  coding: utf-8 
import socketserver
from urllib import parse
import os

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
class MyWebServer(socketserver.BaseRequestHandler):
    

    def parse_request(self, msg):
        split_msg = msg.split("\r\n")
        print(split_msg)
        if 'GET' in split_msg[0]:
            url = split_msg[0].split()[1]
            print("Printing URL")
            print(url)
            print(parse.urlparse(url))
            test = self.do_GET(url)
            self.send_message(200, msg=test)
            return
        else:
            print("send error code")
            self.do_GET(405)



        return

    def send_message(self, code, msg=''):
        if code == 405:
            data = "HTTP/1.1 405 Method Not Allowed\r\n"
            data += "Connection: close\r\n"
            self.request.sendall(bytearray(data, FORMAT))
        elif code == 200:
            data = "HTTP/1.1 200 OK\r\n"
            data += 'Content-Type: text/html\r\n'
            data += 'Connection: close \r\n\r\n'
            data += str(msg)
            
            self.request.sendall(bytearray(data, FORMAT))


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

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
    server.shutdown()
