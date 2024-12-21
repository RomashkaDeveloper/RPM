import json
import torch
import configparser
from transformers import TextStreamer
from model.config_py import *

device = "cuda" if torch.cuda.is_available() else "cpu"

config = configparser.ConfigParser()
config.read('./config.ini')
model = config['SYSTEM']['model']
method = config['SYSTEM']['method']
user = config['USER']['name']

def load_config(CONFIG_FILE):
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)
    
config_json = load_config('scripts/config.json')
characters = config_json['characters']

character = characters[0]['name']
instruction = characters[0]['instruction'].format(character=character, user=user)
scenario = characters[0]['scenario'].format(character=character, user=user)

messages = [
        {"role": "system", "content": instruction + scenario},
    ]

if method == 'transformers':
    from transformers import AutoModelForCausalLM, AutoTokenizer

    model = AutoModelForCausalLM.from_pretrained(model, device_map = device).to(device)
    tokenizer = AutoTokenizer.from_pretrained(model)

else:
    from unsloth import FastLanguageModel

    max_seq_length = 4096
    dtype = 'float16'
    load_in_4bit = True

    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name = model,
        max_seq_length = max_seq_length,
        dtype = dtype,
        load_in_4bit = load_in_4bit,
        device_map=device
    )

    FastLanguageModel.for_inference(model)

tokenizer.chat_template = roleplay_template

text_streamer = TextStreamer(tokenizer, skip_prompt = True)

def getMessage(user_input):
    messages.append({"role": "user", "content": user_input})
    
    inputs = tokenizer.apply_chat_template(
        messages,
        tokenize = True,
        add_generation_prompt = True,
        return_tensors = "pt",
    ).to("cuda")

    outputs = model.generate(
        input_ids = inputs, 
        treamer = text_streamer,
        max_new_tokens = 4096, 
        use_cache = True, 
        temperature = 1.5, 
        min_p = 0.1
    )
    
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    assistant_response = generated_text.split("assistant")[-1].strip()
    
    messages.append({"role": "assistant", "content": assistant_response})

    return assistant_response

while True:
    print(getMessage(input()))