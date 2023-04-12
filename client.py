import socket
import threading
import math
import random

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


def encode(arrString):
    encodedArr = []
    for string in arrString:
        sum = 0
        for i in range(0, 5):
            if string[i].lower() in mapping:
                sum += int(mapping[string[i].lower()] * (37**(5 - i - 1)))
            else:
                sum += int(mapping[' '] * (37**(5 - i - 1)))
        encodedArr.append(int(sum))
    return encodedArr


def convert_string_to_blocks(string):
    size = len(string)
    if (size % 5 != 0):
        string += " " * (5 - (size % 5))
    string += "endom"
    size = len(string)
    return [string[i:i+5] for i in range(0, size, 5)]


def ciphering(encoded_msg, n, e):
    cipher_text = []
    for num in encoded_msg:
        cipher_text.append(pow(num, e, n))
    return cipher_text


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
        send_to_server(plain_text)
    else:
        break
    thread = threading.Thread(target=read)
    thread.start()


#! to end conversation with server
send_to_server(END_CONVERSATION)
