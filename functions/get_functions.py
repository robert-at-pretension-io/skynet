import ast
import inspect
import importlib

from  system_objects.functions import FunctionInfo
import logging

logger = logging.getLogger(__name__)


def load_functions_from_file(file_path) -> [FunctionInfo]:
    # Print the current directory
    # current_directory = os.getcwd()
    # logger.info(f"Current directory: {current_directory}")

    try:
        with open(file_path, 'r') as file:
            file_contents = file.read()
            logger.info(f"file size: {len(file_contents)}")
            try:
                tree = ast.parse(file_contents, type_comments=True)  

                logger.info(f"tree size: {len(tree.body)}")

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
                        logger.info(f"Looking at function: {node.name}")
                        func_name = node.name
                        func_code = compile(ast.Module(body=[node], type_ignores=[]), filename="<ast>", mode="exec")
                        temp_namespace = {**imported_modules}  # Use imported modules
                        exec(func_code, temp_namespace)
                        func = temp_namespace[func_name]
                        sig = inspect.signature(func)
                        arg_types = {param_name: param.annotation for param_name, param in sig.parameters.items()}

                        # Get source code of the function
                        source_code = ast.unparse(node)


                        function_info = FunctionInfo(func_name, file_path, source_code, "")


                        functions.append(function_info)

                return functions
            except SyntaxError as e:
                logger.error(f"Syntax error in {file_path}: {e}")
                return []
            except Exception as e:
                logger.error(f"Error loading functions from {file_path}: {e}")
                return []
    except FileNotFoundError:
        logger.error(f"The file {file_path} was not found.")
        return []
    except IOError:
        logger.error(f"Error reading the file {file_path}.")
        return []
    


def list_functions(functions):
    logger.info("Available functions:")
    for func_name, func_info in functions.items():
        arg_types = func_info['arg_types']
        logger.info(f"Function: {func_name}, Argument Types: {arg_types}")

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
                logger.error(f"Invalid input: {e}")
            except TypeError as e:
                logger.error(e)
            except Exception as e:
                logger.error(f"Error processing input: {e}")

        args.append(converted_value)
    return args

# file_path = 'get_functions.py'  # Replace with your file path
# loaded_functions = load_functions_from_file(file_path)

# # Loop to ask which function to run
# while T"""  """rue:
#     list_functions(loaded_functions)
#     func_name = input("Enter the function name to run (or 'exit' to quit): ")
    
#     if func_name.lower() == 'exit':
#         break

#     if func_name in loaded_functions:
#         func_info = loaded_functions[func_name]
#         func = func_info['function']
#         arg_types = func_info['arg_types']

#         logger.info(f"Function: {func_name}, Argument Types: {arg_types}")

#         # Call the function to get argument values
#         args = get_argument_values(arg_types)
#         kwargs = {}  # Currently, we are not handling keyword arguments

#         # These arguments are already converted to the correct type, no need for eval
#         converted_args = args

#         result = func(*converted_args, **kwargs)
#         logger.info("Result:", result)
#     else:
#         logger.info(f"Function '{func_name}' not found.")

