# cliente.py (Host B)

import xmlrpc.client

# Endereço do servidor
endereco_servidor = "localhost:8000"

# Endereço deste cliente (substitua pela porta correta)
endereco_cliente = "localhost:9001"  # Host B usa 9001

with xmlrpc.client.ServerProxy(f"http://{endereco_servidor}") as server:
    # Registra o cliente no servidor
    server.registra_cliente(endereco_cliente)

    while True:
        # Solicita ao usuário que digite a mensagem
        mensagem = input("Digite a mensagem (ou 'exit' para sair): ")
        if mensagem.lower() == "exit":
            break

        # Cria o dicionário com a mensagem
        msg = {
            "remetente": endereco_cliente,
            "texto": mensagem
        }

        # Chama a função no servidor para processar a mensagem
        resposta = server.processa_mensagem(msg)
        print(resposta)

with xmlrpc.client.ServerProxy(f"http://{endereco_cliente}") as server:
    server.register_function(lambda msg: print(f"Mensagem recebida de {msg['remetente']}: {msg['texto']}"), 'recebe_mensagem')
    print(f"Cliente iniciado em http://{endereco_cliente}")
    server.serve_forever()