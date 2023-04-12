import socket

public_key = 0
n = 0
p = 0
q = 0
phi = 0

mapping = {str(i): i for i in range(10)}
mapping.update({chr(i + 97): i + 10 for i in range(26)})
mapping[' '] = 36
pair_val = {v: k for k, v in mapping.items()}


def init_socket():
    global client, FORMAT, END_CONVERSATION, HEADER
    PORT = 5050
    FORMAT = "utf-8"
    END_CONVERSATION = "DES"
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
            char = pair_val[remainder]
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
                decrypted_msg = decrypt([int(msg)], n, private_key)
                decoded_msg = map_each_char(decrypted_msg)

                if (''.join(decoded_msg) != "endom"):
                    for i in range(0, len(decoded_msg)):
                        message += str(decoded_msg[i])

                else:
                    print("Message : ", message)
                    message = ""
        except Exception as e:
            print(f"Error: {e}")


init_socket()
#! get public key
msg_len = len(client.recv(HEADER).decode(FORMAT))
if msg_len:
    msg_len = int(msg_len)
    msg = client.recv(msg_len).decode(FORMAT)
    public_key = int(msg)
    print("Public key => ", public_key, flush=True)

#! get n
msg_len = len(client.recv(HEADER).decode(FORMAT))
if msg_len:
    msg_len = int(msg_len)
    msg = client.recv(msg_len).decode(FORMAT)
    n = int(msg)
    print("N => ", n, flush=True)
    p, q = prime_factorization(n)
    phi = (p-1)*(q-1)
    private_key = pow(public_key, -1, phi)
    print("p => ", p)
    print("q => ", q)
    print("phi => ", phi)
    print("private => ", private_key)


run()
# print(prime_factorization(3143658127))
