import tkinter as tk
from tkinter import scrolledtext
from model.model import getMessage
from coqui_tts.mayaVoice import getVoice
from PIL import Image, ImageTk

class ChatGUI:
    def __init__(self, master):
        self.master = master
        master.title("Roleplay with AI models Destop by RomashkaDeveloper")
        master.geometry("1280x720")
        icon_path = "icon.ico"
        icon_image = Image.open(icon_path)
        icon_photo = ImageTk.PhotoImage(icon_image)
        master.iconphoto(True, icon_photo)
        self.history = []
        self.tts_enabled = False
        self.master.configure(bg="#282a36")
        self.chat_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=70, height=20)
        self.chat_area.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        self.msg_entry = tk.Entry(master, width=50)
        self.msg_entry.grid(row=1, column=0, padx=10, pady=10)

        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, pady=10)

        self.tts_button = tk.Button(master, text="TTS Off", command=self.toggle_tts)
        self.tts_button.grid(row=1, column=2, pady=10)

    def send_message(self):
        user_message = self.msg_entry.get()
        if user_message:
            self.chat_area.insert(tk.END, f"You: {user_message}\n")
            
            # Convert history to the format expected by getMessage
            formatted_history = [{'role': 'user' if i % 2 == 0 else 'assistant', 'content': msg} 
                                 for pair in self.history for i, msg in enumerate(pair)]
            
            models_answer = getMessage(user_message, formatted_history)
            self.chat_area.insert(tk.END, f"AI: {models_answer}\n\n")
            self.chat_area.see(tk.END)
            
            if self.tts_enabled:
                getVoice(models_answer)
            
            self.history.append((user_message, models_answer))
            if len(self.history) > 10:
                self.history = self.history[-10:]
            
            self.msg_entry.delete(0, tk.END)

    def toggle_tts(self):
        self.tts_enabled = not self.tts_enabled
        self.tts_button.config(text="TTS On" if self.tts_enabled else "TTS Off")

def main():
    root = tk.Tk()
    chat_gui = ChatGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
