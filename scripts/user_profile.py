import os
import configparser
from colorama import Fore, Style, init

init(autoreset=True)

CONFIG_FILE = "./config.ini"
config = configparser.ConfigParser()
config.read(CONFIG_FILE)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print(Fore.CYAN + Style.BRIGHT + """
    ╔══════════════════════════════════════╗
    ║           RPM user profile           ║
    ╚══════════════════════════════════════╝
    """ + Style.RESET_ALL)

def get_user_name():
    return config['USER']['name']

def save_config(config):
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

def show_current_name():
    return config['USER']['name']

def change_name(name):
    config['USER']['name'] = name
    save_config(config)

def main():
    clear_screen()
    print_header()
    print(Fore.LIGHTCYAN_EX + "Your name is " + get_user_name() + Style.RESET_ALL)
    choice = input(Fore.LIGHTGREEN_EX + "Do you wanna change your name? (y/n): " + Style.RESET_ALL)
    if choice.lower() == 'y':
        new_name = input(Fore.YELLOW + "Enter your new name: " + Style.RESET_ALL)
        change_name(new_name)
        print(Fore.LIGHTMAGENTA_EX + "Your name has been changed to " + new_name + Style.RESET_ALL)
    
    input(Fore.RED + "Press Enter to continue..." + Style.RESET_ALL)

if __name__ == "__main__":
    main()