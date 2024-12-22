import os
import json
import configparser
from models.model import Model
from colorama import Fore, Style, init

config = configparser.ConfigParser()
config.read('config.ini')
user_name = config["USER"]["name"]

init(autoreset=True)

def load_config(CONFIG_FILE):
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)
    
config_characters = load_config("scripts/config.json")
config_chats = load_config("scripts/chat.json")
characters = config_characters['characters']
chats = config_chats['chats']

streamer_input = input(Fore.LIGHTBLUE_EX + "Run as streamer? (y/n): " + Style.RESET_ALL)
if streamer_input.lower() == "y":
    use_streamer = True
else:
    use_streamer = False

if not characters:
    print(Fore.RED + "No characters found.")
else:
    a = 1
    for character in characters:
        print(Fore.LIGHTBLUE_EX + f"{a}. {character['name']}" + Style.RESET_ALL)
        a += 1

    index = int(input(Fore.GREEN + "Choose a number of a character you'd like to chat to: " + Style.RESET_ALL)) - 1
    character_name = characters[index]["name"]

def choose_chat():
    a = 1
    print(Fore.LIGHTBLUE_EX + "0. Start a new chat" + Style.RESET_ALL)
    if chats:
        for chat in chats:
            if chat['character'] == character_name:
                print(Fore.LIGHTBLUE_EX + f"{a}. {chat['title']}" + Style.RESET_ALL)
                a += 1

    chat_index = int(input(Fore.GREEN + "Choose a number of a chat: " + Style.RESET_ALL)) - 1
    if chat_index == -1:
        messages = False
    else:
        messages = chats[chat_index]['messages']

    return messages

def help():
    print(Fore.LIGHTGREEN_EX + "Available commands:" + Style.RESET_ALL)
    print(Fore.LIGHTBLUE_EX + "/help - Show this help message" + Style.RESET_ALL)
    print(Fore.LIGHTBLUE_EX + "/save - Save the current conversation" + Style.RESET_ALL)
    print(Fore.LIGHTBLUE_EX + "/load - Load a saved conversation" + Style.RESET_ALL)
    print(Fore.LIGHTBLUE_EX + "/end - End the conversation" + Style.RESET_ALL)

core = Model(index, choose_chat(), use_streamer)
get_message = core.get_message
save_config = core.save_config
get_messages_for_save = core.get_messages_for_save
push_messages = core.push_messages

os.system('cls' if os.name == 'nt' else 'clear')

print(Fore.CYAN + Style.BRIGHT + """
    ╔══════════════════════════════════════╗
    ║               RPM chat               ║
    ╚══════════════════════════════════════╝
    """ + Style.RESET_ALL)

def save():
    title = input(Fore.GREEN + 'Type the title to save: ' + Style.RESET_ALL)
    new_chat = {"title": title, "character": character_name, "messages": get_messages_for_save()}
    config_chats['chats'] = config_chats.get("chats", []) + [new_chat]
    save_config(CONFIG_FILE="scripts/chat.json", config=config_chats)
    print(Fore.CYAN + "The conversation is saved successfully!"+ Style.RESET_ALL)

def load():
    messages = choose_chat()
    push_messages(messages)

def main():
    while True:
        user_input = input(Fore.GREEN + user_name + ": " + Fore.YELLOW)
        if user_input == "/end":
            break
        elif user_input == "/help":
            help()
        elif user_input == "/save":
            save()
        elif user_input == "/load":
            load()
        else:
            if use_streamer:
                print(Fore.GREEN + character_name + ': ' + Fore.YELLOW, end="")
                get_message(user_input)
            else:
                print(Fore.GREEN + character_name + ": " + Fore.YELLOW + get_message(user_input) + Style.RESET_ALL)

if __name__ == "__main__":
    main()