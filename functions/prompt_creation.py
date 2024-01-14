from system_objects.functions import FunctionInfo
from functions.openai_call import return_gpt_response
import logging

logger = logging.getLogger(__name__)

def return_function_options(functions: [FunctionInfo]) -> str:
    function_options = ""
    for function in functions:
        function_options += f"""
    {function.name} : {function.description}
    """
    return function_options

def create_function(function_objective: str, language: str) -> object:
    prompt = f"""Create a function that accomplishes the following: {function_objective}

    Using the {language} programming language.

    it should return a json object with the following properties:

    required_libraries: a list of strings

    source_code: a string containing just the function definition and the function body (no imports or anything else)

    JSON OBJECT:
    """
    try:
        json_object = return_gpt_response(prompt=prompt, return_json_oject=True, retry_count=3)
        if not required_fields(["required_libraries", "source_code"], json_object):
            logger.error("The json object returned from the language model did not contain the required fields.")
            raise ValueError("The json object returned from GPT-3 did not contain the required fields.")
        return json_object
    except Exception as e:
        raise ValueError(f"Error creating function: {e}")

def create_step_list(goal: str) -> object:
    prompt = f"""Describe the steps that would need to be called to accomplishes the following: {goal}

    When coming up with this list, describe "abstract" functions that will be re-useable for other purposes

    return a JSON object with the following property
    
    function_descriptions: a list of strings that describe the functions used to accomplish the goal. Each list item should just describe in plain english what the functions should do.
    
    JSON OBJECT:
    """
    try:
        json_object =  return_gpt_response(prompt=prompt, return_json_oject=True)

        if not required_fields(["function_descriptions"], json_object):
            logger.error("The json object returned from the language model did not contain the required fields.")
            raise ValueError("The json object returned from GPT-3 did not contain the required fields.")
        return json_object
            
    except Exception as e:
        raise ValueError(f"Error creating step list: {e}")
    
def required_fields(fields : [str], json_object: object) -> bool: 
    """Returns true if the required fields are present in the json object"""
    for field in fields:
        if field not in json_object:
            return False
    return True
        
def describe_function(function_string):
    """Returns a description of the function."""
    # Formulate prompt to GPT:
    prompt = f"""Describe the function, using the input variables. Make the description succinct though covering its entire functionality using plain english: 
    
    {function_string}
    
    Description:"""
    try:

        logger.info("Describing function")
        return return_gpt_response(prompt=prompt);
    except Exception as e:
        logger.error(f"Error describing function: {e}")
        raise ValueError("Error describing function.")
