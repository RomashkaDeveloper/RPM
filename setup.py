from prompt_toolkit import Application
from prompt_toolkit.layout.containers import VSplit, HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
import configparser

class ModelSelector:
    def __init__(self):
        self.os_options = ['transformers', 'unsloth']
        self.models = {
            'transformers': ['unsloth/Llama-3.2-1B-Instruct', 'unsloth/Llama-3.2-1B-Instruct-gguf', 'unsloth/Llama-3.2-3B-Instruct', 'unsloth/Llama-3.2-3B-Instruct-gguf', 'Vikhrmodels/Vikhr-Llama-3.2-1B-Instruct', 'Vikhrmodels/Vikhr-Llama-3.3-1B-Instruct'],
            'unsloth': ['unsloth/Llama-3.2-1B-Instruct', 'unsloth/Llama-3.2-3B-Instruct']
        }
        self.selected_os = None
        self.selected_model = None
        self.current_focus = 'os'
        self.os_index = 0
        self.model_index = 0

    def get_os_text(self):
        return [('class:title', ' Select Operating System:\n')] + [
            ('class:item', f' {">" if i == self.os_index else " "} {os}\n')
            for i, os in enumerate(self.os_options)
        ]

    def get_models_text(self):
        if self.selected_os:
            return [('class:title', f' Select Model for {self.selected_os}:\n')] + [
                ('class:item', f' {">" if i == self.model_index else " "} {model}\n')
                for i, model in enumerate(self.models[self.selected_os])
            ]
        return [('class:title', ' Select an OS first')]

    def create_layout(self):
        return Layout(
            HSplit([
                Window(FormattedTextControl(self.get_os_text), wrap_lines=True),
                Window(height=1, char='-'),
                Window(FormattedTextControl(self.get_models_text), wrap_lines=True),
                Window(height=1, char='-'),
                Window(FormattedTextControl(self.get_status), wrap_lines=True)
            ])
        )

    def get_status(self):
        if self.selected_os:
            return [('class:status', f' Selected OS: {self.selected_os}\n'),
                    ('class:status', f' Selected Model: {self.selected_model or "None"}')]
        return [('class:status', ' No OS selected yet')]

    def create_style(self):
        return Style.from_dict({
            'title': '#ansimagenta bold',
            'item': '#ansiwhite',
            'status': '#ansigreen',
        })

    def create_keybindings(self):
        kb = KeyBindings()

        @kb.add('up')
        def _(event):
            if self.current_focus == 'os':
                self.os_index = (self.os_index - 1) % len(self.os_options)
            else:
                self.model_index = (self.model_index - 1) % len(self.models[self.selected_os])
            self.app.invalidate()

        @kb.add('down')
        def _(event):
            if self.current_focus == 'os':
                self.os_index = (self.os_index + 1) % len(self.os_options)
            else:
                self.model_index = (self.model_index + 1) % len(self.models[self.selected_os])
            self.app.invalidate()

        @kb.add('enter')
        def _(event):
            if self.current_focus == 'os':
                self.selected_os = self.os_options[self.os_index]
                self.current_focus = 'models'
                self.model_index = 0
            else:
                self.selected_model = self.models[self.selected_os][self.model_index]
                self.save_to_config()
                event.app.exit()
            self.app.invalidate()

        @kb.add('c-c')
        def _(event):
            event.app.exit()

        return kb

    def save_to_config(self):
        config = configparser.ConfigParser()
        config['MODEL'] = {'model': self.selected_model}
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        if self.os_index == 0:
            os = 'Windows'
        elif self.os_index == 1:
            os = 'Linux'
        config['SYSTEM'] = {'os': os}
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    def run(self):
        self.app = Application(
            layout=self.create_layout(),
            key_bindings=self.create_keybindings(),
            style=self.create_style(),
            full_screen=True
        )
        self.app.run()

if __name__ == '__main__':
    ModelSelector().run()