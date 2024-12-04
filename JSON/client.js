// client.js

const net = require('net'); // Importa o módulo 'net' para trabalhar com conexões TCP
const readline = require('readline').createInterface({ // Importa o módulo 'readline' para ler entrada do usuário
  input: process.stdin,
  output: process.stdout,
});

const client = new net.Socket(); // Cria um socket TCP para o cliente

client.connect(8080, 'localhost', () => { // Conecta o cliente ao servidor na porta 8080
  console.log('Conectado ao servidor'); // Exibe mensagem de conexão no console

  // Função para ler os valores do usuário
  const readValues = () => {
    // Solicita ao usuário que digite 4 valores separados por espaço
    readline.question('Digite 4 valores separados por espaço: ', (input) => {
      const values = input.split(' ').map(Number); // Converte a entrada em um array de números
      // Verifica se a entrada é válida (4 números)
      if (values.length === 4 && values.every(Number.isFinite)) {
        // Cria um objeto JSON com os valores
        const message = { values: values };
        // Envia a mensagem em formato JSON para o servidor
        client.write(JSON.stringify(message));
      } else {
        // Se a entrada for inválida, exibe mensagem de erro e chama a função readValues() novamente
        console.log('Entrada inválida. Digite 4 valores numéricos.');
        readValues();
      }
    });
  };

  readValues(); // Chama a função para ler os valores pela primeira vez

  client.on('data', (data) => { // Define o evento 'data' para lidar com dados recebidos do servidor
    const response = JSON.parse(data); // Analisa a resposta do servidor como JSON
    if (response.error) {
      // Se houver erro na resposta, exibe a mensagem de erro
      console.error(response.error);
    } else {
      // Se a resposta for válida, exibe a média e o ID do cliente
      console.log(`Cliente ${response.clientId}: Média aritmética = ${response.average}`);
    }
    readValues(); // Chama a função para ler novos valores
  });

  client.on('close', () => { // Define o evento 'close' para lidar com o fechamento da conexão
    console.log('Conexão fechada'); // Exibe mensagem de desconexão
    readline.close(); // Fecha a interface de leitura
  });
});