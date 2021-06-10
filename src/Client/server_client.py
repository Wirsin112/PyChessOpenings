import select
import socket
import logging
import time
import uuid
import datetime
import threading
import json
from time import sleep
import bcrypt

# CRYPT SETTINGS
from PyQt5.QtCore import QMetaObject
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
salt = b'$2b$12$djq/vdGik/e.nlUWotW6Au'

# LOGGING CONFIG
logging.basicConfig(format='%(asctime)s :: %(levelname)s :: %(message)s', level=logging.DEBUG)

# SERVER CONFIG
HOST = 'localhost'
PORT = 8888


class Client:
    def __init__(self,parent):
        self.__username = None
        self.__client_socket = None
        self.__socket_lock = threading.Lock()
        self.__connect_to_server()
        self.__last_request = None
        self.__parent = parent
        self.__thread_work = True
        threading.Thread(target=self.__incoming_server_requests_watchdog).start()

    def shut_down(self):
        self.__thread_work = False
    def get_username(self):
        return self.__username

    def set_parent(self,parent):
        self.__parent = parent

    def get_parent(self):
        return self.__parent

    def __connect_to_server(self):
        logging.debug(f'Connecting to server')
        self.__client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.__client_socket.connect((HOST, PORT))
        except ConnectionRefusedError as error:
            logging.error(str(error))

    def __incoming_server_requests_watchdog(self):
        sleep_time = 0.1
        while self.__thread_work:
            msg_arr = self.__read_from_socket()
            if msg_arr is None:
                time.sleep(sleep_time)
                continue
            for msg in msg_arr:
                if msg['request_type'] != 'ping':
                    logging.debug(str(msg))
                if msg['request_type'] == 'response_to_request':
                    if self.__last_request['request_type'] == 'auth_client':
                        if msg['type'] == 'OK':
                            logging.info(f'Logging in')
                            self.__username = msg['username']
                            logging.info(f'Set new username {self.__username}')
                            QMetaObject.invokeMethod(self.__parent, "Open_menu", Qt.QueuedConnection)

                        elif msg['type'] == 'ERROR':
                            logging.error(f'AUTH ERROR: {msg["msg"]}')
                            QMetaObject.invokeMethod(self.__parent, "Display_error_login", Qt.QueuedConnection)
                    else:
                        if msg['type'] == 'OK':
                            logging.info(f'OK')
                            QMetaObject.invokeMethod(self.__parent, "Open_menu", Qt.QueuedConnection)
                        elif msg['type'] == 'ERROR':
                            logging.error(f'{msg["msg"]}')
                if msg['request_type'] == "start_game":
                    self.__parent.oponnet_user_name.setText(msg["opponent"])
                    self.__parent.list_widget.addItem('SYSTEM: Your game against '+msg["opponent"]+' has started')

                    #TODO add color to msg and and funcionality and connect request to cheese board
                if msg['request_type'] == "message":
                    self.__parent.list_widget.addItem(msg['user']+": "+msg["text"])
                if msg['request_type'] == "win":
                    QMetaObject.invokeMethod(self.__parent,'Win',Qt.QueuedConnection)
            time.sleep(sleep_time)

    def __read_from_socket(self):
        self.__lock_acquire()
        ready = select.select([self.__client_socket], [], [], 0.00001)
        if ready[0]:
            msg = self.__client_socket.recv(1024).decode()
        else:
            msg = ''
        self.__lock_release()
        if msg == '' or msg is None:
            return None
        if msg.find('}{'):
            msg = msg.replace('}{', '};{')
            msg = msg.split(';')
        else:
            msg = [msg]

        mess_array = []
        for m in msg:
            msg_dec = json.loads(m)
            if msg_dec['request_type'] != 'ping':
                logging.debug(f'{self} got message: {msg_dec}')
            mess_array.append(msg_dec)
        return mess_array

    def __send_to_socket(self, msg_dict):
        self.__last_request = msg_dict
        response = json.dumps(msg_dict)
        self.__lock_acquire()
        self.__client_socket.send(response.encode())
        logging.debug(f'{self} sent message: {msg_dict}')
        self.__lock_release()

    def __lock_acquire(self):
        self.__socket_lock.acquire()

    def __lock_release(self):
        self.__socket_lock.release()

    def register_user(self, username, email, password):
        password_hash = bcrypt.hashpw(password.encode(), salt).decode()
        msg = {
            'request_type': 'create_client',
            'username': username,
            'email': email,
            'password_hash': str(password_hash)
        }
        self.__send_to_socket(msg)

    def login(self, username, password):

        password_hash = bcrypt.hashpw(password.encode(), salt).decode()
        msg = {
            'request_type': 'auth_client',
            'username': username,
            'password_hash': str(password_hash)
        }
        self.__send_to_socket(msg)

    def find_opponent(self):
        msg ={
            'request_type': 'find_opponent',
            'username': self.__username
        }
        self.__send_to_socket(msg)
    def play_with_bot(self,color,elo):
        msg = {
            'request_type': 'play_with_bot',
            'color': color,
            'elo': elo
        }
        self.__send_to_socket(msg)
    def send_messenge(self,text):
        msg = {
            'request_type': 'message',
            'text': text
        }
        self.__send_to_socket(msg)
if __name__ == "__main__":
    c = Client()
    c.login('oplamo', 'qwerty')
    while True:
        pass

