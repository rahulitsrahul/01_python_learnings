import threading
import time

# Global list accessed by both threads
data = []
flag = False
lock = threading.Lock()

# Function for the other thread to print values from the list
def print_values():
    global flag, data
    while True:
        with lock:
            if data:
                if not flag:
                    flag = True
                time.sleep(1)
                value = data.pop(0)
        if flag:
            print("\nValue popped:", value)
        with lock:
            if not data:
                flag = False

# Creating a daemon thread for printing values
printer_thread = threading.Thread(target=print_values)
printer_thread.daemon = True
printer_thread.start()

# Main thread to receive input and append values to the list
def main():
    global data, flag
    while True:
        if not flag:
            user_input = input("Enter 'y' to append values to the list: ")
            print(f"user_input: {user_input}")
            if user_input == 'y':
                for i in range(11):
                    with lock:
                        data.append(i)
                    time.sleep(0.4)  # Delay of 0.4 seconds between appends

# Creating a daemon thread for the main function
main_thread = threading.Thread(target=main)
main_thread.daemon = True
main_thread.start()

# The program will continue to run as long as the main thread is active
while True:
    pass
