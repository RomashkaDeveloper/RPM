import configparser
from colorama import Fore, Style, init
import os

init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print(Fore.CYAN + Style.BRIGHT + """
    ╔══════════════════════════════════════╗
    ║           RPM Model Setup            ║
    ╚══════════════════════════════════════╝
    """ + Style.RESET_ALL)

def get_user_choice(prompt, options):
    while True:
        print(Fore.YELLOW + prompt)
        for i, option in enumerate(options, 1):
            print(Fore.GREEN + f"{i}. {option}")
        try:
            choice = int(input(Fore.CYAN + "Enter your choice (number): " + Style.RESET_ALL))
            if 1 <= choice <= len(options):
                return choice
            else:
                print(Fore.RED + "Invalid choice. Please try again.")
        except ValueError:
            print(Fore.RED + "Please enter a number.")

def main():
    clear_screen()
    print_header()

    methods = ["transformers", "unsloth", "llama_cpp"]
    method_choice = get_user_choice("Choose your method:", methods)
    method = methods[method_choice - 1]

    clear_screen()
    print_header()

    if method == "transformers":
        models = ["unsloth/Llama-3.2-1B-Instruct", "unsloth/Llama-3.2-3B-Instruct", "SanjiWatsuki/Kunoichi-7B", "custom model"]
    elif method == "unsloth":
        models = ["unsloth/Llama-3.2-1B-Instruct", "unsloth/Llama-3.2-3B-Instruct", "unsloth/gemma-2-9b-bnb-4bit", "custom model"]
    else:  # llama_cpp
        models = ["TheBloke/Kunoichi-7B-GGUF", "custom model"]

    model_choice = get_user_choice("Choose your model:", models)

    if model_choice == len(models):  # custom model
        model = input(Fore.CYAN + "Type your model's name here: " + Style.RESET_ALL)
    else:
        model = models[model_choice - 1]

    if method == "llama_cpp" and model_choice != 1:
        print(Fore.YELLOW + "Other models are not supported yet. Download it by yourself")

    # Save configuration
    config = configparser.ConfigParser()
    config.read('config.ini')
    config['SYSTEM']['model'] = model
    config['SYSTEM']['method'] = method
    with open('./config.ini', 'w') as configfile:
        config.write(configfile)

    print(Fore.GREEN + "\nConfiguration saved successfully!")
    # input(Fore.YELLOW + "Press Enter to exit...")

if __name__ == "__main__":
    main()