import socket
import threading
import math
import random
import sys
import time


PORT = 5050
FORMAT = "utf-8"
END_CONVERSATION = "DES"
HEADER = 64
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
decrypted_timers = []


mapping = {str(i): i for i in range(10)}
mapping.update({chr(i + 97): i + 10 for i in range(26)})
mapping[' '] = 36
pair_val = {v: k for k, v in mapping.items()}


def decode(encodedArr):
    decoded_text = []
    for number in encodedArr:
        string = ''
        while number > 0:
            remainder = number % 37
            char = pair_val[remainder]
            string = char + string
            number //= 37
        decoded_text.append(string)
    return decoded_text


#!#########################################################################################


def generate_e(phi):
    while True:
        x = random.randint(2, phi-1)
        if math.gcd(x, phi) == 1:
            return x


#!#########################################################################################


def decrypt(cipher_text, n, d):
    decrypted_msg = []
    for char in cipher_text:
        decrypted_msg.append(pow(char, d, n))
    return decrypted_msg

#!#########################################################################################


def generate_prime(bits):
    primes = []
    while len(primes) < 2:
        # Generate a random number of the specified number of bits
        num = random.getrandbits(bits)

        # Set the high bit to ensure that the number has the specified number of bits
        num |= 1 << bits-1

        # Check if the number is prime
        if is_prime(num):
            primes.append(num)
    return primes[0], primes[1]

#!#########################################################################################


def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5)+1):
        if num % i == 0:
            return False
    return True

#!#########################################################################################


def send_to_client(msg, client):
    MSG = str(msg).encode(FORMAT)
    msg_len = len(MSG)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' '*(HEADER - len(send_len) -
                      len(str(msg_len))) + str(msg_len).encode(FORMAT)
    client.send(send_len)
    client.send(MSG)
    print("", flush=True)

#!#########################################################################################


def client(conn, addr, clients):
    print(f"{addr} is Connected!", flush=True)
    connected = True
    send_to_client(public_key, conn)
    send_to_client(n, conn)
    message = ""
    while connected:
        msg_len = conn.recv(HEADER).decode(FORMAT)
        if msg_len:
            msg_len = int(msg_len)
            msg = conn.recv(msg_len).decode(FORMAT)
            if msg == END_CONVERSATION:
                connected = False

            # * calc elapsed time
            start = time.time()
            decrypted_msg = decrypt([int(msg)], n, private_key)
            decoded_msg = decode(decrypted_msg)
            end = time.time()
            # decrypted_timers.append(end - start)
            print(end - start)

            if (''.join(decoded_msg) != "endom"):
                for i in range(0, len(decoded_msg)):
                    message += str(decoded_msg[i])
            else:
                print(message)
                message = ""

            sys.stdout.flush()
            if client != conn:
                send_to_client(msg, clients[-1])
    conn.close()

#!#########################################################################################


def start():
    server.listen()
    print(f"Server is listening to {SERVER}", flush=True)
    clients = []

    while True:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=client, args=(conn, addr, clients))
        thread.start()


#!#########################################################################################
arr_bits = []
num_of_bits = int(input("Enter size of bits: "))
arr_bits.append(num_of_bits)
num_of_bits //= 2
p, q = generate_prime(num_of_bits)
# p = 3752310557
# q = 2742279847
n = p*q
phi = (p-1)*(q-1)
public_key = generate_e(phi)
private_key = pow(public_key, -1, phi)
print("Server is starting", flush=True)
start()
