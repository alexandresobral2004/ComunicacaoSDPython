# servidor.py
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Crie o servidor
with SimpleXMLRPCServer(('localhost', 8000),
                        requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    # Registre uma função que calcula a soma de dois números
    def soma(x, y):
        return x + y

    server.register_function(soma, 'soma')

    # Execute o servidor para sempre
    print("Servidor iniciado em http://localhost:8000")
    server.serve_forever()