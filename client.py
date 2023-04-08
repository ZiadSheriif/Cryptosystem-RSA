import random


def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


# Define a function to find the modular multiplicative inverse of a number a mod m
# This is used to calculate the private key

def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

# Define a function to generate the public and private keys given two large prime numbers p and q


def generate_keypair(p, q):
    # Calculate the modulus n
    n = p * q
    # Calculate Euler's totient function phi(n)
    phi = (p-1) * (q-1)
    # Choose a random integer e such that 1 < e < phi(n) and gcd(e, phi(n)) = 1
    e = random.randint(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randint(1, phi)
        g = gcd(e, phi)
    # Calculate the modular multiplicative inverse of e mod phi(n)
    # This is the private key
    d = mod_inverse(e, phi)
    # Return the public and private keys as tuples
    return (n, e), (n, d)

# Define a function to encrypt a plaintext message using the public key


def encrypt(plaintext, public_key):
    n, e = public_key
    # Convert each character in the plaintext to its corresponding Unicode code point
    # Raise each code point to the power of the public key exponent e, modulo the modulus n
    # This produces a list of ciphertext values, each of which is an integer
    ciphertext = [pow(ord(char), e, n) for char in plaintext]
    # Return the ciphertext as a list of integers
    return ciphertext

# Define a function to decrypt a ciphertext message using the private key


def decrypt(ciphertext, private_key):
    n, d = private_key
    # Raise each ciphertext value to the power of the private key exponent d, modulo the modulus n
    # Convert each resulting value back to its corresponding Unicode character
    # This produces a list of plaintext characters
    plaintext = [chr(pow(char, d, n)) for char in ciphertext]
    # Join the plaintext characters together into a single string
    # Return the plaintext string
    return ''.join(plaintext)


# Choose two large prime numbers p and q
p = 17
q = 19

# Generate the public and private keys
public_key, private_key = generate_keypair(p, q)

# Encrypt a plaintext message using the public key
plaintext = "123456789"
ciphertext = encrypt(plaintext, public_key)

# Decrypt the ciphertext message using the private key
decrypted_plaintext = decrypt(ciphertext, private_key)

# Print the public key, private key, plaintext, ciphertext, and decrypted plaintext
print("Public key:", public_key)
print("Private key:", private_key)
print("Plaintext:", plaintext)
print("Ciphertext:", ciphertext)
print("Decrypted plaintext:", decrypted_plaintext)
