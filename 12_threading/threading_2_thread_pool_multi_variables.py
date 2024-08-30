from concurrent.futures import ThreadPoolExecutor, as_completed

# Function to compute the sum, square, and cube of two numbers
def compute_operations(number_1, number_2):
    sum_numbers = number_1 + number_2
    square_sum = sum_numbers ** 2
    cube_sum = sum_numbers ** 3
    return sum_numbers, square_sum, cube_sum

# List of tuples containing pairs of numbers
number_pairs = [(i, i + 1) for i in range(1, 101)]

# Create a ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=4) as executor:
    # Submit tasks to the thread pool
    future_to_pair = {executor.submit(compute_operations, number_1, number_2): (number_1, number_2) for number_1, number_2 in number_pairs}

    # Collect the results as they complete
    results = {}
    for future in as_completed(future_to_pair):
        number_1, number_2 = future_to_pair[future]
        results[(number_1, number_2)] = future.result()

# Print the results
print("Results for pairs of numbers (sum, square of sum, cube of sum):")
print(results)
