# cliente.py

import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    
    while True:
        # Solicita ao usuário que digite a mensagem
        msg = input("Digite a mensagem (ou 'exit' para sair): ")
        if msg.lower() == "exit":
            break
        
        # Envia a mensagem para o servidor
        s.sendall(msg.encode('utf-8'))
        
        # Recebe a resposta do servidor (mensagem com identificação do remetente)
        data = s.recv(1024)
        print(f"Mensagem recebida: {data.decode('utf-8')!r}")