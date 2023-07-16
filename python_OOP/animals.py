class Pet(object):
    no_of_pets = 0  # Class variable
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.increment_pet_count()
    
    def show(self):
        print(f'My name is {self.name}, my age is {self.age}')
    
    def speak(self):
        print("I dont know what to say")
        
    @classmethod
    def increment_pet_count(cls):
        cls.no_of_pets += 1

class Dog(Pet):
    no_of_dogs = 0 # dogs class variable
    
    def __init__(self, name, age, color):
        super().__init__(name, age) # use name and age from parent class
        self.color = color
        self.increment_dog_count()
    
    def speak(self):
        print(f"I am {self.name}, age is {self.age} and my color is {self.color}. Also, I BARK")
        
    @classmethod
    def increment_dog_count(cls):
        cls.no_of_dogs += 1


# Test script
if __name__ == "__main__":
    d1 = Dog('my_name', 15, "White")
    d1.speak()