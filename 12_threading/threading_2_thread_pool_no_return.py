from concurrent.futures import ThreadPoolExecutor
import time


# Function to compute and print the sum of two numbers
def compute_and_print_sum(number_1, number_2):
    sum_numbers = number_1 + number_2
    time.sleep(1)
    print(f"The sum of {number_1} and {number_2} is {sum_numbers}")

start = time.time()
# List of tuples containing pairs of numbers
number_pairs = [(i, i + 1) for i in range(1, 20)]

# Create a ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=8) as executor:
    # Submit tasks to the thread pool
    futures = [executor.submit(compute_and_print_sum, number_1, number_2) for number_1, number_2 in number_pairs]

    # Wait for all futures to complete
    for future in futures:
        future.result()  # Wait for each future to complete

end = time.time()

print("All computations are done.")
print(f"Elapsed: {round((end-start), 2)}")
