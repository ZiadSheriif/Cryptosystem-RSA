import random
import matplotlib.pyplot as plt
import time


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


def prime_factorization(num):
    factors = []
    divisor = 2
    start = time.time()

    while divisor <= num:
        if num % divisor == 0:
            factors.append(divisor)
            num = num / divisor
        else:
            divisor += 1
    end = time.time()
    print("Time ==> ", end - start)

    return factors[0], factors[1]


def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5)+1):
        if num % i == 0:
            return False
    return True


def plotting(num_bits_list, times):
    plt.plot(num_bits_list, times)
    plt.xlabel('Number of bits')
    plt.ylabel('Time (seconds)')
    plt.title('Computation time vs. Number of bits')
    plt.show()


# print(generate_prime(32))
num_bits_list = [8, 16, 32, 64, 128]
timers = [0.0, 0.0, 0.0049855709075927734, 459.7955594062805, 10000]
plotting(num_bits_list, timers)
for bits in num_bits_list:
    print(f"========== {bits} bits ==========\n")
    bits //= 2
    p, q = generate_prime(bits)
    n = p*q
    prime_factorization(n)
    print(f"===========================\n")
