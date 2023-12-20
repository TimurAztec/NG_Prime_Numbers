import concurrent.futures

def is_prime(num: int):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def generate_numbers(start, end):
    simple_numbers = []
    prime_numbers = []

    def process_number(num):
        if is_prime(num):
            prime_numbers.append(num)
        else:
            simple_numbers.append(num)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(process_number, range(start, end + 1))

    return simple_numbers, prime_numbers