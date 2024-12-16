from prompt_toolkit import Application
from prompt_toolkit.layout.containers import VSplit, HSplit, Window, ConditionalContainer
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import TextArea
from prompt_toolkit.filters import Condition
import configparser

class ResetableTextArea(TextArea):
    def reset(self):
        pass

class ModelSelector:
    def __init__(self):
        self.os_options = ['Windows', 'Linux']
        self.models = {
            'Windows': ['unsloth/Llama-3.2-1B-Instruct', 'unsloth/Llama-3.2-1B-Instruct-gguf', 'unsloth/Llama-3.2-3B-Instruct', 'unsloth/Llama-3.2-3B-Instruct-gguf', 'Vikhrmodels/Vikhr-Llama-3.2-1B-Instruct', 'Vikhrmodels/Vikhr-Llama-3.3-1B-Instruct', 'Custom model'],
            'Linux': ['unsloth/Llama-3.2-1B-Instruct', 'unsloth/Llama-3.2-3B-Instruct', 'Model L3', 'Custom model']
        }
        self.selected_os = None
        self.selected_model = None
        self.current_focus = 'os'
        self.os_index = 0
        self.model_index = 0
        self.custom_model_input = TextArea(multiline=False, wrap_lines=False)
        self.show_custom_input = False

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

    def get_status(self):
        if self.selected_os:
            return [('class:status', f' Selected OS: {self.selected_os}\n'),
                    ('class:status', f' Selected Model: {self.selected_model or "None"}')]
        return [('class:status', ' No OS selected yet')]

    def create_layout(self):
        return Layout(
            HSplit([
                Window(FormattedTextControl(self.get_os_text), wrap_lines=True),
                Window(height=1, char='-'),
                Window(FormattedTextControl(self.get_models_text), wrap_lines=True),
                Window(height=1, char='-'),
                Window(FormattedTextControl(self.get_status), wrap_lines=True),
                ConditionalContainer(
                    Window(self.custom_model_input),
                    filter=Condition(lambda: self.show_custom_input)
                )
            ])
        )


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
                selected = self.models[self.selected_os][self.model_index]
                if selected == 'Custom model':
                    self.show_custom_input = True
                    self.app.layout.focus(self.custom_model_input)
                else:
                    self.selected_model = selected
                    self.save_to_config()
                    event.app.exit()
            self.app.invalidate()

        @kb.add('c-c')
        def _(event):
            event.app.exit()

        @kb.add('enter', filter=Condition(lambda: self.show_custom_input))
        def _(event):
            self.selected_model = self.custom_model_input.text
            self.save_to_config()
            event.app.exit()

        return kb

    def save_to_config(self):
        config = configparser.ConfigParser()
        config['MODEL'] = {'model': self.selected_model or self.custom_model_input.text}
        config['SYSTEM'] = {'os': self.selected_os}
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