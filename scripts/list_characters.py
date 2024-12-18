import json

def load_config():
    with open('/home/hitman/RPM/scripts/config.json', 'r') as config_file:
        return json.load(config_file)

# def save_config(config):
#     with open('/home/hitman/RPM/scripts/config.json', 'w') as config_file:
#         json.dump(config, config_file, indent=4)

config = load_config()

# Update configuration
characters = config['characters']

for character in characters:
    print(character['name'])

# print(characters[0]['name'])
# print(characters[1]['name'])

# characters[0]['name'] = 'Eva'

# print(config)
# Save configuration
# save_config(config)