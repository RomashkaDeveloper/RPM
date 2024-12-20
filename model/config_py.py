# import configparser
# config = configparser.ConfigParser()
# config.read('./config.ini')
# user = config['USER']['name']
# character = config['CHARACTER']['name']

roleplay_template = """{{- bos_token }}
{%- set system_message = messages[0]['content'] | trim if messages[0]['role'] == 'system' else '' %}
{%- set messages = messages[1:] if messages[0]['role'] == 'system' else messages %}
{{- "<|start_header_id|>system<|end_header_id|>\n\n" + system_message + "<|eot_id|>" }}
{%- for message in messages %}
{%- if message.role == 'user' %}
{{- '<|start_header_id|>user<|end_header_id|>\n\n' + message['content'] | trim + '<|eot_id|>' }}
{%- elif message.role == 'assistant' %}
{{- '<|start_header_id|>assistant<|end_header_id|>\n\n' + message['content'] | trim + '<|eot_id|>' }}
{%- endif %}{%- endfor %}
{%- if add_generation_prompt %}{{- '<|start_header_id|>assistant<|end_header_id|>\n\n' }}{%- endif %}
"""

# system_message_v1 = f"Your name is {character}. You are a cute girl. Act, think, answer like she does"
