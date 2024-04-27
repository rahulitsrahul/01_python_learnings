import inspect
from IE_algos import *


# # Example usage
# file_path = r"D:/02_my_learnings/01_python_repo/01_python_learnings/23_ohter_algorithms/function_pointers/IE_algos.py"
# function_names = get_function_names_from_file(file_path)
# print("Function names in the file:", function_names)

def get_function_names_of_class(IE_algo_class):
    members = inspect.getmembers(IE_algo_class)
    functions = [name for name, member in members if inspect.isfunction(member) or inspect.ismethod(member)]
    return functions

if __name__ == '__main__':
    image_enhancement_algos = IE_algos()
    functions = get_function_names_of_class(image_enhancement_algos)
    func = getattr(image_enhancement_algos, functions[-1])
    func('img_1.jpg')
    
