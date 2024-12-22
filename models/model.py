import json
import torch
import configparser
from models.config_py import roleplay_template
from transformers import TextStreamer

device = "cuda" if torch.cuda.is_available() else "cpu"

config = configparser.ConfigParser()
config.read('./config.ini')
model_name = config['SYSTEM']['model']
method = config['SYSTEM']['method']
user = config['USER']['name']

class Model:
    def __init__(self, index, messages, use_streamer):
        self.use_streamer = use_streamer
        self.index = index
        config_json = self.load_config('scripts/config.json')
        characters = config_json['characters']

        character = characters[self.index]['name']
        # self.instruction = characters[self.index]['instruction'].format(character=character, user=user)
        self.scenario = characters[self.index]['scenario'].format(character=character, user=user)

        self.check_messages(messages)

        if method == 'transformers':
            from transformers import AutoModelForCausalLM, AutoTokenizer

            self.model = AutoModelForCausalLM.from_pretrained(model_name, device_map=device).to(device).eval()
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        else:
            from unsloth import FastLanguageModel

            max_seq_length = 4096
            dtype = 'float16'
            load_in_4bit = True

            self.model, self.tokenizer = FastLanguageModel.from_pretrained(
                model_name=model_name,
                max_seq_length=max_seq_length,
                dtype=dtype,
                load_in_4bit=load_in_4bit,
                device_map=device
            )

            FastLanguageModel.for_inference(self.model)

        self.tokenizer.chat_template = roleplay_template

        if self.use_streamer:
            self.text_streamer = TextStreamer(self.tokenizer, skip_prompt = True)

    def check_messages(self, messages):
        if messages:
            self.messages = messages
        else:
            self.messages = [
                {"role": "system", "content": self.scenario},
        ]
    
    def load_config(self, CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
        
    def get_messages_for_save(self):
        return self.messages
    
    def save_config(self, CONFIG_FILE, config):
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)

    def push_messages(self, messages):
        self.check_messages(messages)

    def get_message(self, user_input):
        self.messages.append({"role": "user", "content": user_input})
        
        inputs = self.tokenizer.apply_chat_template(
            self.messages,
            tokenize=True,
            add_generation_prompt=True,
            return_tensors="pt",
        ).to(device)

        if self.use_streamer:
            outputs = self.model.generate(
                input_ids=inputs,
                streamer = self.text_streamer,
                max_new_tokens=4096, 
                use_cache=True, 
                temperature=1.5, 
                min_p=0.1
            )
        else:
            outputs = self.model.generate(
                input_ids=inputs, 
                max_new_tokens=4096, 
                use_cache=True, 
                temperature=1.5, 
                min_p=0.1
            )
        
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        assistant_response = generated_text.split("assistant")[-1].strip()
        
        self.messages.append({"role": "assistant", "content": assistant_response})

        if len(self.messages) > 25:
            self.messages = self.messages[-25:]

        if not self.use_streamer:
            return assistant_response