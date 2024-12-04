# servidor.py (Host B)

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xmlrpc.client

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Lista para armazenar os clientes conectados
clientes_conectados = []

with SimpleXMLRPCServer(('localhost', 8000),
                        requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    def registra_cliente(endereco):
        """
        Registra um cliente na lista de clientes conectados.

        Args:
          endereco: O endereço do cliente no formato 'localhost:porta'.

        Returns:
          Uma string confirmando o registro do cliente.
        """
        clientes_conectados.append(endereco)
        print(f"Cliente {endereco} registrado.")
        return "Cliente registrado com sucesso!"

    server.register_function(registra_cliente, 'registra_cliente')

    def processa_mensagem(msg):
        """
        Encaminha a mensagem para todos os clientes registrados.

        Args:
          msg: Um dicionário contendo a mensagem, com as chaves 'remetente' e 'texto'.

        Returns:
          Uma string confirmando o envio da mensagem.
        """
        print(f"Mensagem de {msg['remetente']}: {msg['texto']}")
        for cliente in clientes_conectados:
            try:
                with xmlrpc.client.ServerProxy(f"http://{cliente}") as client:
                    client.recebe_mensagem(msg)
            except Exception as e:
                print(f"Erro ao enviar mensagem para {cliente}: {e}")
        return "Mensagem enviada para todos os clientes."

    server.register_function(processa_mensagem, 'processa_mensagem')

    print("Servidor intermediário iniciado em http://localhost:8000")
    server.serve_forever()



