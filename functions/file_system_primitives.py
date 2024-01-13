import logging

logger = logging.getLogger(__name__)


def read_file(file_path):
    """Reads and returns the content of a file."""
    try:
        logger.info(f"Reading file {file_path}")
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
    except IOError:
        print(f"Error reading the file {file_path}.")

def write_file(file_path, content, mode='w'):
    """Writes content to a file. By default, it overwrites the file.
    
    Args:
    - file_path: Path to the file.
    - content: Content to be written.
    - mode: Writing mode ('w' for overwrite, 'a' for append).
    """
    try:
        logger.info(f"Writing to file {file_path}")
        with open(file_path, mode) as file:
            file.write(content)
    except IOError:
        print(f"Error writing to the file {file_path}.")

def append_to_file(file_path, content):
    """Appends content to the end of a file."""
    write_file(file_path, content, mode='a')

import os

def delete_file(file_path):
    """Deletes a file."""
    try:
        logger.info(f"Deleting file {file_path}")
        os.remove(file_path)
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
    except OSError:
        print(f"Error deleting the file {file_path}.")

def list_files_in_directory(directory):
    """Lists all files in a given directory.

    Args:
    - directory: The path to the directory.

    Returns:
    - A list of file names in the directory.
    """
    try:
        logger.info(f"Listing files in directory {directory}")
        return [file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]
    except FileNotFoundError:
        print(f"Directory {directory} not found.")
        return []
    except OSError as e:
        print(f"Error accessing directory {directory}: {e}")
        return []

def get_current_working_directory():
    """Returns the current working directory."""
    logger.info("Getting current working directory")
    return os.getcwd()

def set_env_variables_with_defaults(env_vars_defaults):
    """
    Sets environment variables to default values if they are not already set.

    Args:
    - env_vars_defaults: A dictionary where keys are environment variable names 
                         and values are the default values for these variables.
    """
    for var, default in env_vars_defaults.items():
        if var not in os.environ:
            if default != "error":
                logger.info(f"Setting environment variable {var} to default value {default}")
                os.environ[var] = default
            else:
                logger.error(f"Environment variable {var} not set. This is a required variable and no default value provided.")
                raise ValueError(f"Environment variable {var} not set. This is a required variable and no default value provided.")


