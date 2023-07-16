class Pet(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def show(self):
        print(f'My name is {self.name}, my age is {self.age}')
    
    def speak(self):
        print("I dont know what to say")

class Dog(Pet):
    def __init__(self, name, age, color):
        super().__init__(name, age) # use name and age from parent class
        self.color = color
    
    def speak(self):
        print(f"I am {self.name}, age is {self.age} and my color is {self.color}. Also, I BARK")
        
