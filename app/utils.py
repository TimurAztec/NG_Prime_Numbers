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

    for num in range(start, end + 1):
        if is_prime(num):
            prime_numbers.append(num)
        else:
            simple_numbers.append(num)

    return simple_numbers, prime_numbers

def generate_fibonacci_numbers(start, end):
    fibonacci_numbers = [1, 1]
    
    while True:
        next_fibonacci = fibonacci_numbers[-1] + fibonacci_numbers[-2]
        if next_fibonacci <= end:
            fibonacci_numbers.append(next_fibonacci)
        else:
            break
    
    fibonacci_numbers = [num for num in fibonacci_numbers if start <= num <= end]
    
    return fibonacci_numbers