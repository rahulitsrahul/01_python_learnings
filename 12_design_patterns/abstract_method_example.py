from abc import ABC, abstractmethod

class Computer(ABC):
    @abstractmethod
    def process(self):
        pass
    
    
class Laptop(Computer):
    def process(self):
        print("Process from Laptop running")
        

if __name__ == "__main__":
    com1 = Laptop()
    com1.process()