from animals import *

if __name__== "__main__":
    my_pet = Pet("brock", 18)
    my_pet.speak()
        
    tim = Dog("tim", 6, "brown")
    tim.speak()
    tim.show()
    print(f"Dogs count: {Dog.no_of_dogs}")
    
    
    