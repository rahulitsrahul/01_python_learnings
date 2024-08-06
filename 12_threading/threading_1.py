import threading
import time
import queue

def print_numbers(start, end):
    for i in range(start, end):
        print(f"numbers {i}")
        time.sleep(1)
        
def print_letters():
    for l in "abcde":
        print(f"letters {l}")
        time.sleep(1)
        
def get_squares(numbers_list, result_queue):
    for number in numbers_list:
        square = number * number
        result_queue.put(square)
        
def get_cube(number, result_dict, lock):
    cube = number**3
    with lock:
        result_dict[number] = cube
    time.sleep(1)
    
        
if __name__ == "__main__":
    # Create Threads
    # Pass parameters to thread
    thread_1 = threading.Thread(target=print_numbers, args=(0, 5))
    # No parameters passed
    thread_2 = threading.Thread(target=print_letters)
    # Return values within queue
    res_queue = queue.Queue()
    thread_3 = threading.Thread(target=get_squares, args = ([1, 2, 3, 4], res_queue))
    
    # Return values within a dictionary
    res_dict = {}
    # Create lock object
    lock = threading.Lock()
    thread_4 = threading.Thread(target=get_cube, args=(3, res_dict, lock))
    thread_5 = threading.Thread(target=get_cube, args=(5, res_dict, lock))
    
    
    # Start Threads
    thread_1.start()
    thread_2.start()
    thread_3.start()
    thread_4.start()
    thread_5.start()
    
    thread_1.join()
    thread_2.join()
    thread_3.join()
    thread_4.join()
    thread_5.join()
    print("Completed jobs, finished Execution")
    
    print ("thread_queue_result")
    for q_item in res_queue.queue:
        print(q_item)
        
    print("Thread_dict_result")
    print(res_dict)