// server.js

const net = require('net'); // Importa o módulo 'net' para trabalhar com conexões TCP

const clients = new Map(); // Cria um Map para armazenar os clientes e seus IDs

const server = net.createServer((socket) => { // Cria um servidor TCP
  // Gera um ID único para o cliente usando Math.random()
  const clientId = Math.random().toString(36).substring(2, 15);
  clients.set(socket, clientId); // Armazena o socket do cliente e seu ID no Map
  console.log(`Cliente ${clientId} conectado`); // Exibe mensagem de conexão no console

  socket.on('data', (data) => { // Define o evento 'data' para lidar com dados recebidos do cliente
    try {
      // Tenta analisar os dados recebidos como JSON
      const message = JSON.parse(data);

      // Verifica se a mensagem contém a propriedade 'values' com 4 valores numéricos
      if (message.values && message.values.length === 4) {
        // Calcula a média aritmética dos valores
        const average = message.values.reduce((sum, value) => sum + value, 0) / 4;

        // Cria um objeto JSON com o ID do cliente e a média calculada
        const response = {
          clientId: clientId,
          average: average,
        };
        // Envia a resposta em formato JSON para o cliente
        socket.write(JSON.stringify(response));
      } else {
        // Se a mensagem for inválida, exibe mensagem de erro no console e envia mensagem de erro para o cliente
        console.log(`Mensagem inválida do cliente ${clientId}`);
        socket.write(JSON.stringify({ error: 'Mensagem inválida' }));
      }
    } catch (error) {
      // Se houver erro ao processar a mensagem, exibe mensagem de erro no console e envia mensagem de erro para o cliente
      console.error(`Erro ao processar mensagem do cliente ${clientId}: ${error}`);
      socket.write(JSON.stringify({ error: 'Erro ao processar mensagem' }));
    }
  });

  socket.on('end', () => { // Define o evento 'end' para lidar com o fechamento da conexão pelo cliente
    clients.delete(socket); // Remove o cliente do Map
    console.log(`Cliente ${clientId} desconectado`); // Exibe mensagem de desconexão no console
  });
});

// Inicia o servidor na porta 8080
server.listen(8080, () => {
  console.log('Servidor escutando na porta 8080');
});