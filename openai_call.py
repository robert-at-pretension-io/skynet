from openai import OpenAI
client = OpenAI(
    # Defaults to os.environ.get("OPENAI_API_KEY")
)

keep_going = True
message_log = []
while keep_going:
    user_input = input("You: ")
    message_log.append({"role": "user", "content": user_input})

    if user_input == "bye":
        keep_going = False
        break

    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=message_log
    )

    #agregate the messages to the chat
    # and the response so the ai has a log of what's been happening
    message_log.append(chat_completion.choices[0].message)


    print("AI: " + chat_completion.choices[0].message.content)
