#!/usr/bin/python3

import getpass
import json
import re
import sys
import termcolor
import threading
import urllib.parse
import urllib.request
from urllib.error import URLError, HTTPError
from InputUtils import Log
from InputUtils import DealJson
from InputUtils import Msg_get_Timer
Name = None
settings = {
    'log_self' : False,
    'url' : {
        'regist' :'http://127.0.0.1:8888/regist',
        'login' : 'http://127.0.0.1:8888/login',
        'send_msg' : 'http://127.0.0.1:8888/send_msg',
        'get_msg'  : 'http://127.0.0.1:8888/get_msg',
        'off' : "http://127.0.0.1:8888/exit",
    },
    'count':None ,
    'user' : None,
}

class MsgPoster(DealJson):
    def __init__(self, server):
        self.server = server

    def post(self, label, msg):
        json_object = {label: json.dumps(msg)}
        self.msg = urllib.parse.urlencode(json_object).encode('utf8')
        
        self.req = urllib.request.Request(self.server, self.msg)
        try:
            response = urllib.request.urlopen(self.req)
        except HTTPError as e:
            print('Error code: ', e.code)
            sys.exit(0)
        except URLError as e:
            print('Error reason: ', e.reason)
            sys.exit(0)
        json_response =  response.read().decode('utf8')
        return self.output(json_response)

class usr_regist(MsgPoster):
    def __init__(self, server=settings['url']['regist']):
        super(usr_regist, self).__init__(server)

    def regist(self):
        mail_pat = re.compile(r'.+?@.+\.+.+\w$')
        self.name = input('UserName: ')
        self.email = input('Email: ')
        if not mail_pat.match(self.email): sys.exit(0)
        self.password = getpass.getpass('Password: ')
        json_object = {
            'name': self.name,
            'email': self.email,
            'password': self.password,
            }
        self.response = self.post(
            'JSON_SIGN', json_object,
            )
        # if self.response.lower() == 'ok':
        print(self.response)
        return self.response
        # print(self.response)


class usr_login(MsgPoster,):
    def __init__(self, server=settings['url']['login']):
        super(usr_login, self).__init__(server)

    def login(self):
        global Name
        
        ### be care of !!!
        global settings  

        self.name = input('UserName: ')
        self.password = getpass.getpass('Password: ')
        
        Name = self.name

        json_object = {
            'name': self.name,
            'password': self.password,
            }
        self.response = self.post(
            'JSON_LOGIN', json_object,
            )

        try:
            settings['user'] = self.name
        except TypeError:
            print ("\n\tprocess exit !!")
            sys.exit(0)

        return self.response
       
class send_msg(MsgPoster):
    def __init__(self,server=settings['url']['send_msg']):
        super(send_msg,self).__init__(server)
        self.name = Name
        self.response = None

    def send(self):


        msg = Log.type_to_all()
        objects = {
            'msg' : msg,
            'name' : self.name,
        }
        self.response = self.post(
            "JSON_MSG",objects,
            )

        if settings['log_self']:
            print (self.response)
        return self.response

class get_msg(MsgPoster):
    """ this is a special class ,
        this class will run in another thread, by Timer

    """
    def __init__(self,server=settings['url']['get_msg']):
        super(get_msg,self).__init__(server)
        self.name = settings['user']
        self.response = None
        try:
            self.local_lines = Log.Count_history()
        except FileNotFoundError:
            self.local_lines = 0
    def capture_msg(self):
        objects = {
            'name' : self.name,
            'i' : self.local_lines,
        } 

        self.response = self.post(
            'JSON_SYNC' ,objects,
            )
        Msg = self.response
        Log.record_in_local(Msg)
        new_count = len(Msg)
        
  
        print ("count : %d"%self.local_lines)
        Log.print_history(Msg)
            
class off_online(MsgPoster):
         """for off_online """
         def __init__(self, server=settings['url']['off']):
            super(off_online, self).__init__(server)
            self.res = self.post(
                'name', settings['name'],
                )
            print (self.res)
            

if __name__ == '__main__':
    try:
        response = usr_login().login()
        
        try:
            status = response['state']
            print(response)
        except TypeError:
            status  = response
            print (status)
        if status == 'ok':
            while True:
                #### use a call back method skill ###
                Msg_get_Timer(get_msg().capture_msg) 
                if( send_msg().send() == 'unlogin'):
                    sys.exit(0)
                
        elif status == 'no such account':
            usr_regist().regist()
        elif status == "already login":
            print ("such account already login in ")
        else :
            print('password error.')
    except EOFError:
        sys.exit(0)
    except KeyboardInterrupt:
        sys.exit(0)
