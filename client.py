import socket
import threading
import time

PORT = 5050
FORMAT = "utf-8"
END_CONVERSATION = "DES"
HEADER = 64
SERVER = socket.gethostbyname(socket.gethostname())
# print(SERVER)
ADDR = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

plain_text = ''
public_key = 0
n = 0
encrypted_timers = []

mapping = {str(i): i for i in range(10)}
mapping.update({chr(i + 97): i + 10 for i in range(26)})
mapping[' '] = 36


def encode(arrString):
    encoded_text = []
    for string in arrString:
        sum = 0
        for i in range(0, 5):
            if string[i].lower() in mapping:
                sum += int(mapping[string[i].lower()] * (37**(5 - i - 1)))
            else:
                sum += int(mapping[' '] * (37**(5 - i - 1)))
        encoded_text.append(int(sum))
    return encoded_text

#!#########################################################################################


def convert_string_to_blocks(string):
    size = len(string)
    if (size % 5 != 0):
        string += " " * (5 - (size % 5))
    string += "endom"
    size = len(string)
    return [string[i:i+5] for i in range(0, size, 5)]

#!#########################################################################################


def ciphering(encoded_msg, n, e):
    cipher_text = []
    for num in encoded_msg:
        cipher_text.append(pow(num, e, n))
    return cipher_text

#!#########################################################################################


def send_to_server(msg):
    converted_msg = convert_string_to_blocks(msg)
    encoded_msg = encode(converted_msg)
    cipher_text = ciphering(encoded_msg, n, public_key)

    for char in cipher_text:
        MSG = str(char).encode(FORMAT)
        msg_len = len(MSG)
        send_len = str(msg_len).encode(FORMAT)
        send_len += b' '*(HEADER - len(send_len))
        client.send(send_len)
        client.send(MSG)

#!#########################################################################################


def read():
    try:
        msg_len = len(client.recv(HEADER).decode(FORMAT))
        if msg_len:
            msg_len = int(msg_len)
            msg = client.recv(msg_len).decode(FORMAT)
    except Exception as e:
        print(f"Error: {e}")


msg_len = len(client.recv(HEADER).decode(FORMAT))
if msg_len:
    msg_len = int(msg_len)
    msg = client.recv(msg_len).decode(FORMAT)
    public_key = int(msg)
    print("Public key => ", public_key, flush=True)


msg_len = len(client.recv(HEADER).decode(FORMAT))
if msg_len:
    msg_len = int(msg_len)
    msg = client.recv(msg_len).decode(FORMAT)
    n = int(msg)
    print("N => ", n, flush=True)
while True:
    plain_text = input("Enter a plain text: ")
    if plain_text != END_CONVERSATION:
        # * calc elapsed time
        start = time.time()
        send_to_server(plain_text)
        end = time.time()
        encrypted_timers.append(end-start)
    else:
        break
    thread = threading.Thread(target=read)
    thread.start()


#! to end conversation with server
send_to_server(END_CONVERSATION)
