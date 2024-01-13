import ast
import inspect
import importlib
from openai_call import return_gpt_response

def addition(a: int, b: int):
    return a + b

import ast
import inspect
import importlib

from ..system_objects.functions import FunctionInfo

def load_functions_from_file(file_path) -> [FunctionInfo]:
    with open(file_path, 'r') as file:
        file_contents = file.read()

    tree = ast.parse(file_contents)
    functions = []
    imported_modules = {}

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for name in node.names:
                imported_modules[name.name] = importlib.import_module(name.name)
        elif isinstance(node, ast.ImportFrom):
            module = importlib.import_module(node.module)
            for name in node.names:
                imported_modules[name.name] = getattr(module, name.name)

        if isinstance(node, ast.FunctionDef):
            func_name = node.name
            func_code = compile(ast.Module(body=[node], type_ignores=[]), filename="<ast>", mode="exec")
            temp_namespace = {**imported_modules}  # Use imported modules
            exec(func_code, temp_namespace)
            func = temp_namespace[func_name]
            sig = inspect.signature(func)
            arg_types = {param_name: param.annotation for param_name, param in sig.parameters.items()}

            # Get source code of the function
            source_code = inspect.getsource(func)


            function_info = FunctionInfo(func_name, file_path, source_code, "")


            functions.append(function_info)

    return functions


def list_functions(functions):
    print("Available functions:")
    for func_name, func_info in functions.items():
        arg_types = func_info['arg_types']
        print(f"Function: {func_name}, Argument Types: {arg_types}")

def get_argument_values(arg_types):
    args = []
    for arg_name, arg_type in arg_types.items():
        while True:
            user_input = input(f"Enter value for {arg_name} ({arg_type}): ")

            try:
                if arg_type == int:
                    converted_value = int(user_input)
                elif arg_type == float:
                    converted_value = float(user_input)
                elif arg_type == bool:
                    converted_value = user_input.lower() in ['true', '1', 'yes']
                elif arg_type == str:
                    converted_value = user_input
                else:
                    # For other types, attempt eval (use cautiously)
                    converted_value = eval(user_input)

                if not isinstance(converted_value, arg_type) and arg_type != inspect._empty:
                    raise TypeError(f"Incorrect type for {arg_name}, expected {arg_type}")

                break  # Break the loop if no error
            except ValueError as e:
                print(f"Invalid input: {e}")
            except TypeError as e:
                print(e)
            except Exception as e:
                print(f"Error processing input: {e}")

        args.append(converted_value)
    return args

# file_path = 'get_functions.py'  # Replace with your file path
# loaded_functions = load_functions_from_file(file_path)

# # Loop to ask which function to run
# while True:
#     list_functions(loaded_functions)
#     func_name = input("Enter the function name to run (or 'exit' to quit): ")
    
#     if func_name.lower() == 'exit':
#         break

#     if func_name in loaded_functions:
#         func_info = loaded_functions[func_name]
#         func = func_info['function']
#         arg_types = func_info['arg_types']

#         print(f"Function: {func_name}, Argument Types: {arg_types}")

#         # Call the function to get argument values
#         args = get_argument_values(arg_types)
#         kwargs = {}  # Currently, we are not handling keyword arguments

#         # These arguments are already converted to the correct type, no need for eval
#         converted_args = args

#         result = func(*converted_args, **kwargs)
#         print("Result:", result)
#     else:
#         print(f"Function '{func_name}' not found.")

def describe_function(function_string):
    """Returns a description of the function."""
    # Formulate prompt to GPT:
    prompt = f"""Describe the function, using the input variables. Make the description succinct though covering its entire functionalijty using plain english: 
    
    {function_string}
    
    Description:"""

    return_gpt_response(prompt=prompt);
