import socket
import threading
import random

# adresa IP si portul serverului
HOST = '127.0.0.1'
PORT = 5050

# lista de clienti conectati la server, fiecare client fiind o pereche de socket si nume
clients = []

# numarul maxim de incercari permise
MAX_TRIES = 15

# functia de joc
def play_game(client_name, client_socket):
    # generarea numarului de ghicit
    target_number = ''.join(random.sample('0123456789', 4))

    # initializarea contorului de incercari
    tries = 0

    # jocul continua pana cand numarul este ghicit sau numarul maxim de incercari este atins
    while True:
        # primirea solutiei clientului
        guess = client_socket.recv(1024).decode().strip()

        # verificarea daca solutia este valida
        if len(guess) != 4 or not guess.isdigit() or len(set(guess)) != 4:
            client_socket.sendall('Solutie invalida\n'.encode())
            continue

        # incrementarea numarului de incercari
        tries += 1

        # verificarea daca numarul a fost ghicit
        if guess == target_number:
            # notificarea tuturor clientilor despre ghicirea numarului
            message = f'{client_name} a ghicit numarul {target_number} din {tries} incercari\n'
            print(message)
            for c in clients:
                c[0].sendall(message.encode())

            # generarea unui nou numar si reluarea jocului
            target_number = ''.join(random.sample('0123456789', 4))
            tries = 0
        else:
            # determinarea numarului de cifre centrate si necentrate
            centered = sum(1 for x, y in zip(guess, target_number) if x == y)
            not_centered = sum(min(guess.count(x), target_number.count(x)) for x in set(guess)) - centered

            # trimiterea raspunsului clientului
            client_socket.sendall(f'{centered}C{not_centered}N\n'.encode())

            # verificarea daca numarul maxim de incercari a fost atins
            if tries == MAX_TRIES:
                # notificarea tuturor clientilor despre depasirea numarului maxim de incercari
                message = f'{client_name} a depasit numarul maxim de incercari pentru numarul {target_number}\n'
                print(message)
                for c in clients:
                    c[0].sendall(message.encode())

                # generarea unui nou numar si reluarea jocului
                target_number = ''.join(random.sample('0123456789', 4))
                tries = 0

    # inchiderea conexiunii cu clientul
    client_socket.close()

# functia pentru acceptarea clientilor
def accept_clients():
    while True:
        # acceptarea conexiunii unui client nou
        client_socket, client_address = server_socket.accept()

        # primirea numelui clientului
        client_name = client_socket.recv(1024).decode()

        # verificarea daca numele clientului este unic
        if any(client_name == c[1] for c in clients):
            client_socket.sendall('Numele este deja folosit\n'.encode())
            client_socket.close()
            continue

        # adaugarea clientului la lista de clienti
        clients.append((client_socket, client_name))

        # notificarea celorlalti clienti despre clientul nou
        print(f'{client_name} s-a conectat')
        for c in clients:
            if c != (client_socket, client_name):
                c[0].sendall(f'{client_name} s-a conectat\n'.encode())

        # pornirea jocului pentru clientul nou intr-un thread separat
        threading.Thread(target=play_game, args=(client_name, client_socket)).start()


#crearea socket-ului serverului
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

#pornirea serverului
server_socket.listen()

#acceptarea clientilor intr-un thread separat
threading.Thread(target=accept_clients).start()

#afisarea mesajului de pornire a serverului
print(f'Server-ul a pornit pe adresa {HOST}:{PORT}')