import random


def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None


def generate_keypair(p, q):
    n = p * q
    phi = (p-1) * (q-1)
    e = random.randint(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randint(1, phi)
        g = gcd(e, phi)
    d = mod_inverse(e, phi)
    return (n, e), (n, d)


def encrypt(plaintext, public_key):
    n, e = public_key
    ciphertext = [pow(ord(char), e, n) for char in plaintext]
    return ciphertext


def decrypt(ciphertext, private_key):
    n, d = private_key
    plaintext = [chr(pow(char, d, n)) for char in ciphertext]
    return ''.join(plaintext)


p = 17
q = 19
public_key, private_key = generate_keypair(p, q)

plaintext = "Ziad"
ciphertext = encrypt(plaintext, public_key)
decrypted_plaintext = decrypt(ciphertext, private_key)

print("Public key:", public_key)
print("Private key:", private_key)
print("Plaintext:", plaintext)
print("Ciphertext:", ciphertext)
print("Decrypted plaintext:", decrypted_plaintext)
