from concurrent.futures import ThreadPoolExecutor, as_completed
import math
import time

# Function to compute the square root of a single number
def compute_sqrt(number):
    time.sleep(1)
    return math.sqrt(number)


if __name__ == "__main__":
    # List of numbers from 1 to 100
    numbers = list(range(1, 25))
    
    start = time.time()
    # Create a ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=8) as executor:
        # Submit tasks to the thread pool
        future_to_number = {executor.submit(compute_sqrt, number): number for number in numbers}
    
        # Collect the results as they complete
        results = [None] * len(numbers)
        results_dict = {}
        for future in as_completed(future_to_number):
            number = future_to_number[future]
            index = numbers.index(number)
            results[index] = future.result()
            results_dict[number] = future.result()
            
    end = time.time()
    
    # Print the results
    print("Square roots of numbers from 1 to 100:")
    print(results)
    print(f"Execution_time: {round(end-start, 3)} sec")