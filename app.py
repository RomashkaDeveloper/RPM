import os
import subprocess
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print(Fore.CYAN + Style.BRIGHT + """
    ╔══════════════════════════════════════╗
    ║             RPM Console              ║
    ╚══════════════════════════════════════╝
    """ + Style.RESET_ALL)

def print_menu():
    print(Fore.YELLOW + "Choose an action:")
    print(Fore.GREEN + "1. Create a character")
    print(Fore.GREEN + "2. List characters")
    print(Fore.GREEN + "3. Choose a character")
    print(Fore.GREEN + "4. User profile")
    print(Fore.GREEN + "5. Model settings")
    print(Fore.RED + "6. Exit")

def execute_script(script_name):
    try:
        subprocess.run(["python", script_name], check=True)
    except subprocess.CalledProcessError:
        print(Fore.RED + f"Error executing {script_name}")
    except FileNotFoundError:
        print(Fore.RED + f"File {script_name} not found")
    input(Fore.YELLOW + "\nPress Enter to continue...")

def main():
    while True:
        clear_screen()
        print_header()
        print_menu()
        
        choice = input(Fore.CYAN + "\nEnter your choice (1-6): " + Style.RESET_ALL)
        
        if choice == '1':
            execute_script("create_character.py")
        elif choice == '2':
            execute_script("scripts/list_characters.py")
        elif choice == '3':
            execute_script("choose_character.py")
        elif choice == '4':
            execute_script("user_profile.py")
        elif choice == '5':
            execute_script("scripts/setup.py")
        elif choice == '6':
            print(Fore.YELLOW + "\nThank you for using RPM Console. Goodbye!")
            break
        else:
            print(Fore.RED + "\nInvalid choice. Please try again.")
            input(Fore.YELLOW + "Press Enter to continue...")

if __name__ == "__main__":
    main()