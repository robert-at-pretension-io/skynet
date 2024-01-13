
from functions.get_functions import load_functions_from_file, list_functions, get_argument_values, get_function_names, get_function_info

from functions.file_system_primitives import read_file, write_file, append_to_file, delete_file, list_files_in_directory, get_current_working_directory, set_env_variables_with_defaults

from system_objects.functions import FunctionInfo, load_function_infos_from_file, save_function_infos_to_file

import os

# Example usage
env_vars_defaults = {
    "OPENAI_API_KEY": "error",
    "DEFAULT_GPT_MODEL": "gpt-3.5-turbo-1106",
    "FUNCTIONS_FOLDER": "functions",
    "FUNCTION_INFO_SERIALIZATION_FILES": "serialized_function_info.json",
}

try: 
    set_env_variables_with_defaults(env_vars_defaults)
except Exception as e:
    print(f"Error setting environment variables: {e}")

# Make sure the functions are loaded
files_in_functions_folder = list_files_in_directory(env_vars_defaults["FUNCTIONS_FOLDER"])
functions = []

for file in files_in_functions_folder:
    if file.endswith(".py"):
        functions : [FunctionInfo]= load_functions_from_file(os.path.join(env_vars_defaults["FUNCTIONS_FOLDER"], file))

from system_objects.functions import FunctionInfo

existing_function_info : [FunctionInfo] = []
# Try to load the existing function info from FUNCTION_INFO_SERIALIZATION_FILES . First check if that file exists, if not, create it.

if os.path.exists(env_vars_defaults["FUNCTION_INFO_SERIALIZATION_FILES"]):
    existing_function_info = load_function_infos_from_file(env_vars_defaults["FUNCTION_INFO_SERIALIZATION_FILES"])
else:
    #create the file
    save_function_infos_to_file(functions, env_vars_defaults["FUNCTION_INFO_SERIALIZATION_FILES"])

