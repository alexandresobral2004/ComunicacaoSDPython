# cliente.py
import xmlrpc.client

s = xmlrpc.client.ServerProxy('http://localhost:8000')

# Envia dois números para o servidor e recebe a soma
num1 = 10
num2 = 5
resultado = s.soma(num1, num2)

print(f"A soma de {num1} e {num2} é: {resultado}")