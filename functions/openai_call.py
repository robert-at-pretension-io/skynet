from openai import OpenAI
import os

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



def return_gpt_response(message_log = [], prompt = "", model = ""):
    # If both are empty, throw error
    if message_log == [] and prompt == "":
        raise ValueError("Both message_log and prompt cannot be empty when calling return_chat_response.")
    
    if model == "":
        model = os.environ["DEFAULT_GPT_MODEL"]
    
    # if the prompt is not empty, add it to the message log
    if prompt != "":
        message_log.append({"role": "user", "content": prompt})
    # Send the message log to the AI
    chat_completion = client.chat.completions.create(
        model=model,
        messages=message_log
    )
    # Add the response to the message log
    return chat_completion.choices[0].message.content


