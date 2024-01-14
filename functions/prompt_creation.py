from system_objects.functions import FunctionInfo
from functions.openai_call import return_gpt_response
import logging

logger = logging.getLogger(__name__)

def return_function_options(functions: [FunctionInfo]) -> str:
    function_options = ""
    for function in functions:
        function_options += f"{function.name} : {function.description}\n"
    return function_options

def create_function(function_objective: str, language: str) -> object:
    prompt = f"""Create a function that accomplishes the following: {function_objective}

    Using the {language} programming language.

    it should return a json object with the following properties:

    required_libraries: a list of strings

    source_code: a string

    The source code should ONLY be the function definition, including the function definition and the function body.
    """
    try:
        json_oject = return_gpt_response(prompt=prompt, return_json_oject=True)
        if not required_fields(["required_libraries", "source_code"], json_oject):
            logger.error("The json object returned from the language model did not contain the required fields.")
            raise ValueError("The json object returned from GPT-3 did not contain the required fields.")
        return json_oject
    except Exception as e:
        raise ValueError(f"Error creating function: {e}")

def create_step_list(goal: str, functions: [str]) -> object:
    prompt = f"""Create a step list that accomplishes the following: {goal}

    Note that you can only use the command line on the ubuntu operating system, and you can only use the following python functions:

    {return_function_options(functions)}

    The json object returned should have the following properties:
    step_list: a list of strings describing the steps to accomplish the goal
    """


    try:
        json_object =  return_gpt_response(prompt=prompt, return_json_oject=True)

        if not required_fields(["step_list"], json_object):
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
