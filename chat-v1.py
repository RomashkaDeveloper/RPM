import os
import json
from model import Model
from colorama import Fore, Style, init

init(autoreset=True)

def load_config(CONFIG_FILE):
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)
    
config_json = load_config('scripts/config.json')
characters = config_json['characters']

a = 1
for character in characters:
    print(Fore.LIGHTMAGENTA_EX + f"{a}. {character['name']}" + Style.RESET_ALL)
    a += 1

index = int(input(Fore.GREEN + "Choose a number of a character you'd like to chat to: " + Style.RESET_ALL)) - 1

getMessage = Model(index).getMessage

os.system('cls' if os.name == 'nt' else 'clear')

print(Fore.CYAN + Style.BRIGHT + """
    ╔══════════════════════════════════════╗
    ║               RPM chat               ║
    ╚══════════════════════════════════════╝
    """ + Style.RESET_ALL)

while True:
    user_input = input(Fore.GREEN + 'You: ' + Style.RESET_ALL)
    print(Fore.YELLOW + getMessage(user_input) + Style.RESET_ALL)
