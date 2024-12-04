# servidor.py

import socket
import threading

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

def handle_client(conn, addr):
    """
    Lida com a conexão de um cliente.

    Args:
      conn: Objeto de conexão do socket.
      addr: Endereço do cliente.
    """
    print(f"[NOVA CONEXÃO] {addr} conectado.")
    conectado = True
    while conectado:
        try:
            # Recebe a mensagem do cliente
            msg = conn.recv(1024).decode('utf-8')
            if msg:
                if msg.lower() == "exit":
                    conectado = False
                else:
                    # Encaminha a mensagem para todos os outros clientes
                    broadcast(msg, conn)
            else:
                # Se nenhuma mensagem for recebida, remove o cliente
                remove_client(conn)
                conectado = False
        except:
            remove_client(conn)
            conectado = False

def broadcast(msg, conn):
    """
    Encaminha a mensagem para todos os clientes, exceto o remetente.

    Args:
      msg: Mensagem a ser enviada.
      conn: Conexão do cliente remetente.
    """
    for client in clients:
        if client != conn:
            try:
                # Inclui o endereço do remetente na mensagem
                client.send(f"[{conn.getpeername()}] {msg}".encode('utf-8'))
            except:
                # Remove o cliente se houver erro ao enviar a mensagem
                remove_client(client)

def remove_client(conn):
    """
    Remove um cliente da lista de clientes.

    Args:
      conn: Conexão do cliente a ser removido.
    """
    if conn in clients:
        clients.remove(conn)
        print(f"[DESCONEXÃO] {conn.getpeername()} desconectado.")

# Lista para armazenar as conexões dos clientes
clients = []

# Cria o socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"[ESCUTANDO] Servidor escutando em {HOST}:{PORT}")

    while True:
        # Aceita a conexão de um cliente
        conn, addr = s.accept()
        
        # Adiciona o cliente à lista de clientes
        clients.append(conn)

        # Inicia uma nova thread para lidar com o cliente
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[CONEXÕES ATIVAS] {threading.activeCount() - 1}")