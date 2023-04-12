import random


def generate_prime(bits):
    while True:
        # Generate a random number of the specified number of bits
        num = random.getrandbits(bits)

        # Set the high bit to ensure that the number has the specified number of bits
        num |= 1 << bits-1

        # Check if the number is prime
        if is_prime(num):
            return num


def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5)+1):
        if num % i == 0:
            return False
    return True


# print(generate_prime(32))
print(is_prime(3752310557))
