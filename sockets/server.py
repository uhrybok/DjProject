import socket

HOST = ('127.0.0.1', 7007)

# SOCK_DGRAM - UDP,  SOCK_STREAM - TCP, AF_INET - ip v4
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(HOST)
sock.listen()

print("--start server--")

running = True

while running:
    conn, addr = sock.accept()    

    while 1:
        data = conn.recv(1024).decode()
        print('client', addr, 'said:',data)
    
        if data.lower() == 'bye':
            break

        if data.lower() == 'stop':
            running = False
            break

    conn.close()

sock.close()

print("--stop server--")
