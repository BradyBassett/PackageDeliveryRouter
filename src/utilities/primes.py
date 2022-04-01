def generate_next_prime(num):
    if num <= 1:
        return 2

    while True:
        num += 1
        if is_prime(num):
            return num


def is_prime(num):
    if num % 2 == 0:
        return False
    for i in range(3, int(num**0.5 + 1), 2):
        if num % i == 0:
            return False
    return True
