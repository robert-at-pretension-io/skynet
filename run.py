
from functions.get_functions import load_functions_from_file, list_functions, get_argument_values, get_function_names, get_function_info, describe_function

from functions.file_system_primitives import read_file, write_file, append_to_file, delete_file, list_files_in_directory, get_current_working_directory, set_env_variables_with_defaults

from system_objects.functions import FunctionInfo, load_function_infos_from_file, save_function_infos_to_file

import os

import logging
import config.log_config

logger = logging.getLogger()


env_vars_defaults = {
    "OPENAI_API_KEY": "error",
    "DEFAULT_GPT_MODEL": "gpt-3.5-turbo-1106",
    "FUNCTIONS_FOLDER": "functions",
    "FUNCTION_INFO_SERIALIZATION_FILES": "serialized_function_info.json",
}

def load_env_vars(defaults):
    try:
        logger.info("Loading environment variables")
        set_env_variables_with_defaults(defaults)
    except Exception as e:
        logger.error(f"Error loading environment variables: {e}")


def load_functions() -> [FunctionInfo]:
    # Make sure the functions are loaded
    try:
        files_in_functions_folder = list_files_in_directory(env_vars_defaults["FUNCTIONS_FOLDER"])
    except:
        logger.error(f"Error loading functions from {env_vars_defaults['FUNCTIONS_FOLDER']}")
        raise ValueError(f"Error loading functions from {env_vars_defaults['FUNCTIONS_FOLDER']}")
    
    functions : [FunctionInfo]= []

    for file in files_in_functions_folder:
        if file.endswith(".py"):
            functions : [FunctionInfo]= load_functions_from_file(os.path.join(env_vars_defaults["FUNCTIONS_FOLDER"], file))

    from system_objects.functions import FunctionInfo

    existing_function_info : [FunctionInfo] = []
    # Try to load the existing function info from FUNCTION_INFO_SERIALIZATION_FILES . First check if that file exists, if not, create it.

    if os.path.exists(env_vars_defaults["FUNCTION_INFO_SERIALIZATION_FILES"]):
        try:
            existing_function_info = load_function_infos_from_file(env_vars_defaults["FUNCTION_INFO_SERIALIZATION_FILES"])
        except:
            logger.error(f"Error loading existing function info from {env_vars_defaults['FUNCTION_INFO_SERIALIZATION_FILES']}")
            raise ValueError(f"Error loading existing function info from {env_vars_defaults['FUNCTION_INFO_SERIALIZATION_FILES']}")
    else:
        #create the file
        try: 
            save_function_infos_to_file(functions, env_vars_defaults["FUNCTION_INFO_SERIALIZATION_FILES"])
        except:
            logger.error(f"Error creating file {env_vars_defaults['FUNCTION_INFO_SERIALIZATION_FILES']}")
            raise ValueError(f"Error creating file {env_vars_defaults['FUNCTION_INFO_SERIALIZATION_FILES']}")

    existing_function_names = [function_info.function_name for function_info in existing_function_info]

    # Check if the functions variables are in the "existing_function_info" array If not, get the description from GPT and add it to the array. Then save the array to the file.

    for function in functions:
        if function.name not in existing_function_names:
            print(f"Adding function {function.function_name} to existing function info"`)
            # Get the description from GPT
            description = describe_function(function.source_code)

            print(f"Came up with the description: {description} for the function {function.function_name}")

            existing_function_info.append(FunctionInfo(function.function_name, function.file_name, function.source_code , description))

    # Overide the existing function info file with the new function info
    save_function_infos_to_file(existing_function_info, env_vars_defaults["FUNCTION_INFO_SERIALIZATION_FILES"])

    return existing_function_info


def main():
    logger.info("Skynet started")
    load_env_vars(env_vars_defaults)

if __name__ == '__run__':
    main()