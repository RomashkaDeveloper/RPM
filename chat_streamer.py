import json
from model.streamer_model import Model

def load_config(CONFIG_FILE):
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)
    
config_json = load_config('scripts/config.json')
characters = config_json['characters']

config_chat = load_config('scripts/chat.json')
chats = config_chat['chats']

a = 1
for character in characters:
    print(f"{a}. {character['name']}")
    a += 1

index = int(input("Choose a number of a character you'd like to chat to: ")) - 1

a = 1
print("0. Start a new chat")
for chat in chats:
    print(f"{a}. {chat['title']}")
    a += 1

chat_index = int(input("Choose a number of a chat: ")) - 1
if chat_index == -1:
    messages = False
else:
    messages = chats[chat_index]['messages']

def help():
    print("Available commands:")
    print("/help - Show this help message")
    print("/save - Save the current conversation")
    print("/end - End the conversation")

getMessage = Model(index, messages).getMessage

while True:
    user_input = input("You: ")
    if user_input == "/end":
        break
    elif user_input == "/help":
        help()
    elif user_input == "/save":
        title = input('Type the title to save: ')
    getMessage(user_input)