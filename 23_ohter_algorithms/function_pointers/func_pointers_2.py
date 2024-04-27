import inspect

def func1():
    pass

def func2():
    pass

def func3():
    pass

# Get all function names in the current module
function_names = [name for name, obj in inspect.getmembers(__import__(__name__)) if inspect.isfunction(obj)]

print(function_names)