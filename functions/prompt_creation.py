from ..system_objects.functions import FunctionInfo
from openai_call import return_gpt_response

def return_function_options(functions: [FunctionInfo]) -> str:
    function_options = ""
    for function in functions:
        function_options += f"{function.function_name} : {function.description}\n"
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
        return return_gpt_response(prompt=prompt, return_json_oject=True)
    except Exception as e:
        raise ValueError(f"Error creating function: {e}")

def create_step_list(goal: str) -> object:
    prompt = f"""Create a step list that accomplishes the following: {goal}

    The json object returned should have the following properties:
    step_list: a list of strings describing the steps to accomplish the goal
    verification: a string describing how to verify that the goal has been accomplished
    """
    try:
        return return_gpt_response(prompt=prompt, return_json_oject=True)
    except Exception as e:
        raise ValueError(f"Error creating step list: {e}")
