import json
import os
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

CONFIG_FILE = 'scripts/config.jsonl'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print(Fore.CYAN + Style.BRIGHT + """
    ╔══════════════════════════════════════╗
    ║        RPM Character Manager         ║
    ╚══════════════════════════════════════╝
    """ + Style.RESET_ALL)

def print_menu():
    print(Fore.YELLOW + "Choose an action:")
    print(Fore.GREEN + "1. List characters")
    print(Fore.GREEN + "2. Create a character")
    print(Fore.GREEN + "3. Delete a character")
    print(Fore.RED + "4. Exit")

def load_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"characters": []}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def list_characters(config):
    clear_screen()
    characters = config.get("characters", [])
    if not characters:
        print(Fore.YELLOW + "No characters found.")
    else:
        print(Fore.CYAN + "Characters:")
        for i, character in enumerate(characters, 1):
            print(Fore.GREEN + f"{i}. {character['name']}")

def create_character(config):
    clear_screen()
    name = input(Fore.CYAN + "Enter character name: " + Style.RESET_ALL)
    instruction = input(Fore.CYAN + "Enter character instruction or type \"default\": " + Style.RESET_ALL)
    if instruction == "default":
        instruction = "Text transcript of a never-ending conversation between {user} and {character}"
    scenario = input(Fore.CYAN + "Enter character scenario: " + Style.RESET_ALL)
    new_character = {"name": name, "instruction": instruction, "scenario": scenario}
    config["characters"] = config.get("characters", []) + [new_character]
    save_config(config)
    print(Fore.GREEN + f"Character '{name}' created successfully!")

def delete_character(config):
    clear_screen()
    characters = config.get("characters", [])
    if not characters:
        print(Fore.YELLOW + "No characters to delete.")
        return

    list_characters(config)
    try:
        choice = int(input(Fore.CYAN + "Enter the number of the character to delete: " + Style.RESET_ALL))
        if 1 <= choice <= len(characters):
            deleted_character = characters.pop(choice - 1)
            save_config(config)
            print(Fore.GREEN + f"Character '{deleted_character['name']}' deleted successfully!")
        else:
            print(Fore.RED + "Invalid choice.")
    except ValueError:
        print(Fore.RED + "Please enter a valid number.")

def main():
    while True:
        clear_screen()
        print_header()
        print_menu()
        
        choice = input(Fore.CYAN + "\nEnter your choice (1-4): " + Style.RESET_ALL)
        
        config = load_config()
        
        if choice == '1':
            list_characters(config)
        elif choice == '2':
            create_character(config)
        elif choice == '3':
            delete_character(config)
        elif choice == '4':
            print(Fore.YELLOW + "\nExiting Character Manager. Goodbye!")
            break
        else:
            print(Fore.RED + "\nInvalid choice. Please try again.")
        
        input(Fore.YELLOW + "\nPress Enter to continue...")

if __name__ == "__main__":
    main()