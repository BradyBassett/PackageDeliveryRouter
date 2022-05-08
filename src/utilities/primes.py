def generate_next_prime(num: int) -> int:
    """
    Function to generate the next prime number after the given parameter.\n
    Space complexity O(1)\n
    Time complexity O(N)
    """
    if num <= 1:
        return 2

    while True:
        num += 1
        if is_prime(num):
            return num


def is_prime(num: int) -> bool:
    """
    Function to determine if a given integer is prime.\n
    Space complexity O(1)\n
    Time complexity O(N)
    """
    if num % 2 == 0:
        return False
    for i in range(3, int(num**0.5 + 1), 2):
        if num % i == 0:
            return False
    return True
