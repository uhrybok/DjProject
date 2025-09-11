import socket


HOST = ('127.0.0.1', 7007)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect(HOST)

    print("--start client--")

    while 1:
        text = input("Enter message (or 'bye' or 'stop'): ")
        sock.sendall(text.encode("utf-8"))
    
        if text.lower() == 'bye' or text.lower() == 'stop':
            break

    sock.close()
except:
    print("connection error")    

print("--stop client--")