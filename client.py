import socket

# definirea adresei si portului serverului
HOST = '127.0.0.1'
PORT = 5050

# primirea numele clientului
name = input('Introdu numele tau: ')

# conectarea la server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))

    # trimiterea numelui clientului la server
    client_socket.sendall(name.encode())

    while True:
        # primirea solutiei de la client
        guess = input('Introdu solutia ta (un numar de patru cifre diferite): ')

        # trimiterea solutiei la server
        client_socket.sendall(guess.encode())

        # primirea raspunsului de la server
        response = client_socket.recv(1024).decode()

        if not response:
            break

        print(response)

        # daca clientul a ghicit numarul, iesim din bucla
        if '4 centered' in response:
            break

print('Conexiunea cu serverul a fost inchisa')
