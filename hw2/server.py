'''
написать приложение-сервер используя модуль socket работающее в домашней 
локальной сети.
Приложение должно принимать данные с любого устройства в сети отправленные 
или через программу клиент или через браузер
    - если данные пришли по протоколу http создать возможность след.логики:
        - если путь "/" - вывести главную страницу
        
        - если путь содержит /test/<int>/ вывести сообщение - тест с номером int запущен
        
        - если путь содержит message/<login>/<text>/ вывести в консоль/браузер сообщение
            "{дата время} - сообщение от пользователя {login} - {text}"
        
        - если путь содержит указание на файл вывести в браузер этот файл
        
        - во всех остальных случаях вывести сообщение:
            "пришли неизвестные  данные по HTTP - путь такой то"
                   
         
    - если данные пришли НЕ по протоколу http создать возможность след.логики:
        - если пришла строка формата "command:reg; login:<login>; password:<pass>"
            - выполнить проверку:
                login - только латинские символы и цифры, минимум 6 символов
                password - минимум 8 символов, должны быть хоть 1 цифра
            - при успешной проверке:
                1. вывести сообщение на стороне клиента: 
                    "{дата время} - пользователь {login} зарегистрирован"
                2. добавить данные пользователя в список/словарь на сервере
            - если проверка не прошла вывести сообщение на стороне клиента:
                "{дата время} - ошибка регистрации {login} - неверный пароль/логин"
                
        - если пришла строка формата "command:signin; login:<login>; password:<pass>"
            выполнить проверку зарегистрирован ли такой пользователь на сервере:                
            
            при успешной проверке:
                1. вывести сообщение на стороне клиента: 
                    "{дата время} - пользователь {login} произведен вход"
                
            если проверка не прошла вывести сообщение на стороне клиента:
                "{дата время} - ошибка входа {login} - неверный пароль/логин"
        
        - во всех остальных случаях вывести сообщение на стороне клиента:
            "пришли неизвестные  данные - <присланные данные>"       
                 

'''

import socket
import os
import json
from datetime import datetime

HOST = ('127.0.0.1', 7007)

OK = b'HTTP/1.1 200 OK\n'
HEADERS = b"Host: djproject.py\nContent-Type: text/html; charset=utf-8\n\n"
ERR_404 = b'HTTP/1.1 404 Not Found\n\n'
USERS_PATH = "hw2/users.json"

def path_type(path):
    # print(f"path <{path}>")
    first = path.split("/", 1)[0]

    if first == "test":
        return "test"
    elif first == "message":
        return "message"
    else:
        full_path = os.path.join(os.path.dirname(__file__), path)
        if os.path.isfile(full_path) == True or os.path.isdir(full_path) == True:
            return "file"
    
    return ""

def send_file(conn, path):
    full_path = os.path.join(os.path.dirname(__file__), path)
    if os.path.isdir(full_path) == True:
        full_path = os.path.join(full_path, "index.html")
    else:
        ext =  full_path.split(".")[-1]
        if ext not in ['webp', 'jpg', 'png', 'gif', 'ico', 'txt', 'html', 'json']:
            conn.send(ERR_404)
            return None

    with open(full_path.lstrip('/'), 'rb') as f:                   
        conn.send(OK)
        conn.send(HEADERS)
        conn.send(f.read())

def run_test(path):
    try:
        test_num = int(path.split("/", 2)[1])
        print(f"- Test #{test_num} launched -")
    except:
        print(f"- invalid data - \n path: <{path}>")

def print_message(path):
    try:
        data = path.split("/", 3)
        print(f"- {datetime.now()} - user message {data[1]} - {data[2]} -")
    except:
        print(f"- invalid data - \n path: <{path}>")

def process_http(conn, data):
    header = data.split('\n')[0].split(" ", 2)
    method = header[0]
    path = header[1]    

    if method == "GET":
        path = path.lstrip('/')
        p_type = path_type(path)
        # print(p_type)
        if p_type == "file":
            send_file(conn, path)
        elif p_type == "test":
            run_test(path)
        elif p_type == "message":
            print_message(path)
        else:
            print(f"- invalid data - \n path: <{path}>")
    else:
        print("- method not supported -")    

def check_reg(comm):
    message = "Registration error"

    with open(USERS_PATH, "r", encoding="utf-8") as j:
        try:
            users = json.load(j)
        except:
            users = []
    
    if any(entry["login"] == comm["login"] for entry in users):
        message = f"username <{comm["login"]}> is taken"
    else:
        users.append({
            "login": comm["login"], 
            "password": comm["password"]
        })    
        with open(USERS_PATH, "w", encoding="utf-8") as j:
            json.dump(users, j, ensure_ascii=False, indent=4)
            message = f"{datetime.now()} Ueser {comm["login"]} registred"

    return message

def check_signin(comm):
    message = "Log in error"

    with open(USERS_PATH, "r", encoding="utf-8") as j:
        try:
            users = json.load(j)
        except:
            users = []

    user = next((u for u in users if u["login"] == comm["login"]), None)
    
    if user:
        if user["password"] == comm["password"]:
            message = f"{datetime.now()} Ueser {comm["login"]} logged in"
        else:    
            message = f"Incorrect password"
    else:
        message = f"Username <{comm["login"]}> not found"
    
    return message

def run_command(conn, data):
    message = f"- invalid data: <{data}> -"

    try:
        comm = dict(item.strip().split(":", 1) for item in data.split(";"))
        # print(comm)

        if comm["command"] == "reg":
            message = check_reg(comm)
        elif comm["command"] == "signin":
            message = check_signin(comm) 
    finally:
        conn.send(message.encode("utf-8"))

def is_http(data):
    res = False
    try:
        protocol = data.split('\n')[0].split(" ")[2][:4]
        # print(protocol)
        if protocol == "HTTP":
            res = True
    finally:
        return res

def process_data(conn, data):
    print(f"client {addr} said <{data}>")

    if data:
        if is_http(data):
            process_http(conn, data)
        else:
            run_command(conn, data)

# SOCK_DGRAM - UDP,  SOCK_STREAM - TCP, AF_INET - ip v4
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

    sock.bind(HOST)
    sock.listen()

    print("-- start server --")

    while 1:
        conn, addr = sock.accept()    
        data = conn.recv(1024).decode()
        process_data(conn, data)
        conn.close()

print("--stop server--")
