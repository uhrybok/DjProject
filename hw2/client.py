"""

написать приложение-клиент используя модуль socket работающее в домашней 
локальной сети.
Приложение должно соединятся с сервером по известному адрес:порт и отправлять 
туда текстовые данные.

известно что сервер принимает данные следующего формата:
    "command:reg; login:<login>; password:<pass>" - для регистрации пользователя
    "command:signin; login:<login>; password:<pass>" - для входа пользователя
    
    
с помощью программы зарегистрировать несколько пользователей на сервере и произвести вход


"""
import socket


HOST = ('127.0.0.1', 7007)

print("-- start client --")

while 1:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(HOST)

        command = input("Enter 'reg', 'signin' or 'exit'): ").lower()

        if command == 'exit':
            break
        elif command == 'reg' or command == 'signin':
            login = input("Login: ")
            password = input("Password: ")
            sock.sendall(f"command:{command}; login:{login}; password:{password}".encode("utf-8"))
            # print(f"command:{command}; login:<{login}>; password:<{password}>")
        else:
            sock.sendall(f"command:{command}".encode("utf-8"))
            # print("- Incorrect command -")

        data = sock.recv(1024).decode() 
        print(data) 

print("-- stop client --")