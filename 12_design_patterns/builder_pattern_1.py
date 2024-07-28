from abc import ABC, abstractmethod

class Car:
    def __init__(self):
        self.engine = None
        self.wheels = None
        self.color = None
        
    def __str__(self):
        return f"car with Engine: {self.engine}, Wheels: {self.wheels}, Color: {self.color}"
        
class CarBuilder(ABC):
    @abstractmethod
    def set_engine(self, engine_type):
        pass
    
    @abstractmethod
    def set_wheels(self, wheel_type):
        pass
    
    @abstractmethod
    def set_color(self, color):
        pass
    
    @abstractmethod
    def get_car(self):
        pass
    

class SUV_CarBuilder(CarBuilder):
    def __init__(self):
        self.car = Car()
        
    def set_engine(self, engine_type):
        self.car.engine = engine_type
        
    def set_wheels(self, wheel_type):
        self.car.wheels = wheel_type
    
    def set_color(self, color):
        self.car.color = color
        
    def get_car(self):
        return self.car
        

class sports_CarBuilder(CarBuilder):
    def __init__(self):
        self.car = Car()
        
    def set_engine(self, engine_type):
        self.car.engine = engine_type
        
    def set_wheels(self, wheel_type):
        self.car.wheels = wheel_type
    
    def set_color(self, color):
        self.car.color = color
        
    def get_car(self):
        return self.car
        

class Car_Director:
    def __init__(self, builder):
        self.builder = builder
        
    def construct(self, engine_type, wheel_type, color):
        self.builder.set_engine(engine_type)
        self.builder.set_wheels(wheel_type)
        self.builder.set_color(color)
    
if __name__ == "__main__":
    # Create a sports car
    sports_car_builder = sports_CarBuilder()
    director = Car_Director(sports_car_builder)
    director.construct(engine_type="V8", wheel_type="Alloy", color="Red")
    sports_car = sports_car_builder.get_car()
    print(sports_car)
    
    
    # Create a SUV car
    suv_car_builder = SUV_CarBuilder()
    director = Car_Director(suv_car_builder)
    director.construct(engine_type="V6", wheel_type="Steel", color="blue")
    SUV_car = suv_car_builder.get_car()
    print(SUV_car)
    
    
    
    
    
        
        

