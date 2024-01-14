
from functions.get_functions import load_functions_from_file

from functions.prompt_creation import create_function, create_step_list, describe_function

from functions.file_system_primitives import append_to_file, list_files_in_directory, set_env_variables_with_defaults

from system_objects.functions import FunctionInfo, load_function_infos_from_file, save_function_infos_to_file

import os

import logging

import config.log_config

logger = logging.getLogger(__name__)


env_vars_defaults = {
    "OPENAI_API_KEY": "error",
    # "DEFAULT_GPT_MODEL": "gpt-3.5-turbo-1106",
    "DEFAULT_GPT_MODEL": "gpt-4-1106-preview",
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
        logger.info(f"Loaded functions from {env_vars_defaults['FUNCTIONS_FOLDER']}")
    except:
        logger.error(f"Error loading functions from {env_vars_defaults['FUNCTIONS_FOLDER']}")
        raise ValueError(f"Error loading functions from {env_vars_defaults['FUNCTIONS_FOLDER']}")
    
    functions : [FunctionInfo]= []

    for file in files_in_functions_folder:
        if file.endswith(".py"):
            file_path = os.path.join("./", env_vars_defaults["FUNCTIONS_FOLDER"], file)
            try: 
                logger.info(f"Trying to load functions from {file_path}")
                #append to the functions array
                more_functions = load_functions_from_file(file_path)

                functions.extend(more_functions)

                logger.info(f"Loaded {len(more_functions)} functions from {file_path}")
            except Exception as e:
                logger.error(f"Error loading functions from {file_path}: {e}")
                raise ValueError(f"Error loading functions from {file}: {e}")
                

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

    existing_function_names = [function_info.name for function_info in existing_function_info]

    # Check if the functions variables are in the "existing_function_info" array If not, get the description from GPT and add it to the array. Then save the array to the file.

    for function in functions:
        if function.name not in existing_function_names:
            print(f"Adding function {function.name} to existing function info")
            # Get the description from GPT
            description = describe_function(function.source_code)

            print(f"Came up with the description: {description} for the function {function.name}")

            existing_function_info.append(FunctionInfo(function.name, function.file_location, function.source_code , description))

    # Overide the existing function info file with the new function info
    save_function_infos_to_file(existing_function_info, env_vars_defaults["FUNCTION_INFO_SERIALIZATION_FILES"])

    return existing_function_info


def main():
    logger.info("Skynet started")
    load_env_vars(env_vars_defaults)
    functions = load_functions()

    logger.info(f"The following {len(functions)} function(s) were loaded: {[function.name for function in functions]}")

    # Start the chat loop
    keep_going = True
    while keep_going:
        user_input = input("What goal would you like to accomplish?")

        if user_input == "bye":
            keep_going = False
            break
        else:
            try:
                json_object = create_step_list(user_input)
                print(f"Here are the functions needed to accomplish {user_input}:")
                for required_function in json_object["function_descriptions"]:
                    print(required_function)

                    # Create a function that accomplishes this task:
                    function_def_json_object = create_function(required_function, "python")
                    source_code = function_def_json_object["source_code"] + "\n\n"


                    required_libraries = function_def_json_object["required_libraries"]
                    # append the source code to a file ./functions/generated_functions.py

                    for library in required_libraries:
                        logger.info(f"Make sure the library {library} is installed")

                    append_to_file("./functions/generated_functions.py", source_code)

                    


            except: 
                logger.error(f"Error creating step list for {user_input}")
                raise ValueError(f"Error creating step list for {user_input}")


if __name__ == '__main__':
    main()