import inspect

def check_greet(name):
    print("Hello,", name)


# Get all function names in the current module
function_names = [name for name, obj in inspect.getmembers(__import__(__name__)) if inspect.isfunction(obj)]

print(function_names)

functions = [func_name for func_name in function_names if func_name.startswith('check_')]


# Calling the function using its name as a string and passing variables
for function_name in functions:
    func = globals()[function_name]
    variable_to_pass = 'rahul'
    func(variable_to_pass)