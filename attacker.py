import socket
import threading


public = 0
n = 0
p = 0
q = 0
phi = 0

mapping = {
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'a': 10,
    'b': 11,
    'c': 12,
    'd': 13,
    'e': 14,
    'f': 15,
    'g': 16,
    'h': 17,
    'i': 18,
    'j': 19,
    'k': 20,
    'l': 21,
    'm': 22,
    'n': 23,
    'o': 24,
    'p': 25,
    'q': 26,
    'r': 27,
    's': 28,
    't': 29,
    'u': 30,
    'v': 31,
    'w': 32,
    'x': 33,
    'y': 34,
    'z': 35,
    ' ': 36
}
inverse_mapping = {v: k for k, v in mapping.items()}


def init_socket():
    global client, FORMAT, D, HEADER
    PORT = 5050
    FORMAT = "utf-8"
    D = "DES"
    HEADER = 64
    SERVER = socket.gethostbyname(socket.gethostname())
    # print(SERVER)
    ADDR = (SERVER, PORT)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)


# return message , M=C^d mod n
def decrypt(cipherArr, n, d):
    decrypted_msg = []
    for C in cipherArr:
        decrypted_msg.append(pow(C, d, n))
    return decrypted_msg


'''takes an array of integers and converts them back to 
the original plaintext messages using a mapping of integers to 
characters. The mapping is based on the ASCII character set,
with the addition of a space character and some lowercase letters.'''
#! 3lashan msh kol el chars allowed 36 chars only!!


def map_each_char(encoded_msg):
    mapped_chars = []
    for number in encoded_msg:
        string = ''
        while number > 0:
            remainder = number % 37
            char = inverse_mapping[remainder]
            string = char + string
            number //= 37
        mapped_chars.append(string)
    return mapped_chars

# *calculate the value of phi, which is needed to calculate the private key
# ? d=e^-1 mod phi(n)

# ? phi(n)=(p-1)(q-1),but n=p*q


def prime_factorization(num):
    factors = []
    divisor = 2

    while divisor <= num:
        if num % divisor == 0:
            factors.append(divisor)
            num = num / divisor
        else:
            divisor += 1

    return factors[0], factors[1]


def run():
    message = ""
    while True:
        try:
            msg_len = len(client.recv(HEADER).decode(FORMAT))
            if msg_len:
                msg_len = int(msg_len)
                msg = client.recv(msg_len).decode(FORMAT)
                decrypted_msg = decrypt([int(msg)], n, d)
                decoded_msg = map_each_char(decrypted_msg)

                if (''.join(decoded_msg) != "endom"):
                    for i in range(0, len(decoded_msg)):
                        message += str(decoded_msg[i])

                else:
                    print("Decoded message : ", message)
                    message = ""
        except Exception as e:
            print(f"Error: {e}")
        # handle the error gracefully, e.g. by closing the connection


init_socket()
#! get public key
msg_len = len(client.recv(HEADER).decode(FORMAT))
# msg_len = False
if msg_len:
    msg_len = int(msg_len)
    msg = client.recv(msg_len).decode(FORMAT)
    public = int(msg)
    print("Public key -> ", public)

#! get n
msg_len = len(client.recv(HEADER).decode(FORMAT))
# msg_len = False
if msg_len:
    msg_len = int(msg_len)
    msg = client.recv(msg_len).decode(FORMAT)
    n = int(msg)
    print("n -> ", n)
    p, q = prime_factorization(n)
    phi = (p-1)*(q-1)
    d = pow(public, -1, phi)
    print("p -> ", p)
    print("q -> ", q)
    print("phi -> ", phi)
    print("private -> ", d)


run()
print(prime_factorization(35))

# while True:
# thread = threading.Thread(target=read)
# thread.start()

# encoded_msg = [36745, 39429, 4380, 31925, 31925, 39429, 31925, 39429, 31925, 39429, 31925, 39429, 31925, 39429,
#                31925, 39429, 31925, 39429, 31925, 39429, 31925, 39429, 31925, 39429, 31925, 39429, 31925, 39429, 31925, 39429]

# mapped_chars = map_each_char(encoded_msg)

# decoded_message = ''.join(mapped_chars)

# print(decoded_message)
