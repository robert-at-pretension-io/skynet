
import requests
from bs4 import BeautifulSoup

def get_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = [a.get('href') for a in soup.find_all('a', href=True)]
    return links



from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers.sql import SqlLexer
from prompt_toolkit.shortcuts import set_title
from prompt_toolkit.styles import Style

# Function to process user input commands
def process_command(command):
    # Split the command into tokens (words)
    tokens = command.split()
    # Handle the 'add' command
    if tokens[0] == 'get_links':
        try:
            # Convert arguments to integers and sum them
            # There should only be one link:
            links = get_links(tokens[1])
            return links
        except ValueError:
            # Return error message for invalid input
            return "Error: Please provide valid numbers."
    elif tokens[0] == 'exit':
        # Return None to signal exit
        return None
    else:
        # Handle unknown commands
        return "Unknown command"

# Set up auto-completion for commands
sql_completer = WordCompleter(['get_links', 'exit'], ignore_case=True)

# Define style for the application
style = Style.from_dict({
    'completion-menu.completion': 'bg:#008888 #ffffff',
    'completion-menu.completion.current': 'bg:#00aaaa #000000',
    'scrollbar.background': 'bg:#88aaaa',
    'scrollbar.button': 'bg:#222222',
})

# Create a prompt session with custom lexer, completer, and style
session = PromptSession(lexer=PygmentsLexer(SqlLexer), completer=sql_completer, style=style)

# Set the title of the terminal window (works in some terminals)
set_title("Skynet")

# Main loop: Continuously prompt user for input
while True:
    try:
        # Prompt the user for input
        text = session.prompt('> ')
    except KeyboardInterrupt:
        # Handle Ctrl+C (KeyboardInterrupt), continue without action
        continue
    except EOFError:
        # Handle Ctrl+D (EOFError), break the loop to exit
        break

    # Process the entered command
    result = process_command(text)

    # If the result is a list, print each item separately
    if isinstance(result, list):
        for item in result:
            print(item)

    if result is None:  # Check for 'exit' command
        break
    else:
        # Print the result of command processing
        print(result)

# Print a goodbye message upon exiting the loop
print('Goodbye!')
