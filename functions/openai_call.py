import json
from openai import OpenAI
import os

import logging

logger = logging.getLogger(__name__)



client = OpenAI(
    # Defaults to os.environ.get("OPENAI_API_KEY")
)

# keep_going = True
# message_log = []
# while keep_going:
#     user_input = input("You: ")
#     message_log.append({"role": "user", "content": user_input})

#     if user_input == "bye":
#         keep_going = False
#         break

#     chat_completion = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=message_log
#     )

#     #agregate the messages to the chat
#     # and the response so the ai has a log of what's been happening
#     message_log.append(chat_completion.choices[0].message)


#     print("AI: " + chat_completion.choices[0].message.content)



def return_gpt_response(message_log = [], prompt = "", model = "", return_json_oject = False, retry_count = 0):
    # If both are empty, throw error
    if message_log == [] and prompt == "":
        raise ValueError("Both message_log and prompt cannot be empty when calling return_chat_response.")
    
    if model == "":
        model = os.environ["DEFAULT_GPT_MODEL"]
    
    # if the prompt is not empty, add it to the message log
    if prompt != "":
        message_log.append({"role": "user", "content": prompt})
        logger.info(f"\nSending Prompt:\n{prompt}\n\n")
    # Send the message log to the AI
        
    if return_json_oject:
        chat_completion = client.chat.completions.create(
            model=model,
            messages=message_log,
            response_format={ "type": "json_object" },
        )
        try:
            logger.info(f"Converting response {chat_completion.choices[0]} to json object")
            return_value = json.loads(chat_completion.choices[0].message.content)
            return return_value
        except:
            if retry_count <= 0:
                logger.error("The response from the AI could not be converted to a json object.")
                raise ValueError("The response from the AI could not be converted to a json object.")
            else:
                logger.log("Couldn't parse response from AI to json object. Re-trying")
                return return_gpt_response(message_log, prompt, model, return_json_oject, retry_count - 1)
    else:
        chat_completion = client.chat.completions.create(
            model=model,
            messages=message_log,
        )
        return chat_completion.choices[0].message.content


