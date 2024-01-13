import json
import inspect
import logging

logger = logging.getLogger(__name__)

class FunctionInfo:
    def __init__(self, function_name, file_location, source_code, description):
        self.name = function_name
        self.file_location = file_location
        self.source_code = source_code
        self.description = description

    def serialize(self):
        """Serializes the instance to a JSON string."""
        data = {
            'function_name': self.name,
            'file_location': self.file_location,
            'source_code': self.source_code,
            'description': self.description
        }
        return json.dumps(data)

    @staticmethod
    def deserialize(json_str):
        """Deserializes a JSON string into a FunctionInfo instance."""
        data = json.loads(json_str)
        function_name = data['function_name']
        file_location = data['file_location']
        source_code = data['source_code']
        description = data['description']
        return FunctionInfo(function_name, file_location, source_code, description)

    @staticmethod
    def _type_to_str(type_obj):
        """Converts a type object to a string."""
        return type_obj.__name__ if type_obj is not None else 'None'

    @staticmethod
    def _str_to_type(type_str):
        """Converts a string back to a type object."""
        return getattr(__builtins__, type_str, None)

def load_function_infos_from_file(file_path):
    """
    Loads a list of serialized FunctionInfo objects from a file.

    Args:
    - file_path: The path to the file from which the data will be loaded.

    Returns:
    - A list of FunctionInfo instances.
    """
    try:
        logger.info(f"Loading function infos from {file_path}")
        with open(file_path, 'r') as file:
            serialized_function_infos = json.load(file)
            return [FunctionInfo.deserialize(json_str) for json_str in serialized_function_infos]
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
        return []
    except IOError as e:
        print(f"Error reading the file {file_path}: {e}")
        return []

def save_function_infos_to_file(function_infos, file_path):
    """
    Saves a list of serialized FunctionInfo objects to a file.

    Args:
    - function_infos: A list of serialized FunctionInfo objects (JSON strings).
    - file_path: The path to the file where the data will be saved.
    """
    try:
        logger.info(f"Saving function infos to {file_path}")
        with open(file_path, 'w') as file:
            json.dump(function_infos, file)
    except IOError as e:
        print(f"Error writing to the file {file_path}: {e}")
