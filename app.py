import tkinter as tk
from tkinter import scrolledtext, font as tkFont  # Added font
import threading
import json
import os
import base64 # Added for encoding/decoding
from openai_client import get_openai_response

CONFIG_FILE = "config.json"

# Define a color scheme (loosely inspired by ChatGPT dark mode)
BG_COLOR = "#343541"  # Main background
FG_COLOR = "#FFFFFF"  # General text color
INPUT_BG_COLOR = "#40414F" # Background for input areas
TEXT_AREA_BG_COLOR = "#40414F" # Background for text display areas (like chat history)
TEXT_AREA_FG_COLOR = "#D1D5DB" # Text color for chat
BUTTON_BG_COLOR = "#4A4E69" # A muted button color
BUTTON_FG_COLOR = "#FFFFFF"
STATUS_BAR_BG_COLOR = "#202123"
STATUS_BAR_FG_COLOR = "#D1D5DB"
USER_MSG_TAG_BG = "#40414F" # Keep same as input for consistency for now
AI_MSG_TAG_BG = BG_COLOR # Slightly different or same, let's try same as main BG

class App:
    def __init__(self, root):
        self.root = root
        root.title("OpenAI API Client")
        root.configure(bg=BG_COLOR)

        # Define fonts
        self.default_font = tkFont.Font(family="Arial", size=10)
        self.chat_font = tkFont.Font(family="Arial", size=11)
        self.label_font = tkFont.Font(family="Arial", size=10, weight="bold")

        config = self.load_config()

        # --- Configuration Frame ---
        config_frame = tk.Frame(root, bg=BG_COLOR, padx=10, pady=10)
        config_frame.grid(row=0, column=0, sticky="ew")
        root.grid_columnconfigure(0, weight=1) # Allow config frame to expand

        # API Key
        tk.Label(config_frame, text="API Key:", bg=BG_COLOR, fg=FG_COLOR, font=self.label_font).grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.api_key_entry = tk.Entry(config_frame, width=60, show='*', bg=INPUT_BG_COLOR, fg=FG_COLOR, insertbackground=FG_COLOR, font=self.default_font)
        self.api_key_entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        self.api_key_entry.insert(0, config.get("api_key", ""))

        # Base URL
        tk.Label(config_frame, text="Base URL:", bg=BG_COLOR, fg=FG_COLOR, font=self.label_font).grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.base_url_entry = tk.Entry(config_frame, width=60, bg=INPUT_BG_COLOR, fg=FG_COLOR, insertbackground=FG_COLOR, font=self.default_font)
        self.base_url_entry.grid(row=1, column=1, padx=5, pady=2, sticky="ew")
        self.base_url_entry.insert(0, config.get("base_url", "https://api.openai.com/v1"))

        # Model Name
        tk.Label(config_frame, text="Model Name:", bg=BG_COLOR, fg=FG_COLOR, font=self.label_font).grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.model_name_entry = tk.Entry(config_frame, width=60, bg=INPUT_BG_COLOR, fg=FG_COLOR, insertbackground=FG_COLOR, font=self.default_font)
        self.model_name_entry.grid(row=2, column=1, padx=5, pady=2, sticky="ew")
        self.model_name_entry.insert(0, config.get("model_name", "gpt-3.5-turbo"))

        # Temperature & Max Length in a sub-frame for better layout
        param_frame = tk.Frame(config_frame, bg=BG_COLOR)
        param_frame.grid(row=3, column=1, sticky="ew", padx=5, pady=2)
        param_frame.grid_columnconfigure(1, weight=1)
        param_frame.grid_columnconfigure(3, weight=1)


        tk.Label(config_frame, text="Temp:", bg=BG_COLOR, fg=FG_COLOR, font=self.label_font).grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.temperature_entry = tk.Entry(param_frame, width=10, bg=INPUT_BG_COLOR, fg=FG_COLOR, insertbackground=FG_COLOR, font=self.default_font)
        self.temperature_entry.grid(row=0, column=0, sticky="w", padx=0, pady=2)
        self.temperature_entry.insert(0, config.get("temperature", "0.7"))

        tk.Label(param_frame, text="Max Resp Len:", bg=BG_COLOR, fg=FG_COLOR, font=self.label_font).grid(row=0, column=1, sticky="w", padx=(10,2), pady=2)
        self.max_length_entry = tk.Entry(param_frame, width=10, bg=INPUT_BG_COLOR, fg=FG_COLOR, insertbackground=FG_COLOR, font=self.default_font)
        self.max_length_entry.grid(row=0, column=2, sticky="w", padx=0, pady=2)
        self.max_length_entry.insert(0, config.get("max_length", "150"))

        config_frame.grid_columnconfigure(1, weight=1) # Allow entry widgets to expand

        # --- Chat History Area ---
        chat_frame = tk.Frame(root, bg=BG_COLOR, padx=10, pady=5)
        chat_frame.grid(row=1, column=0, sticky="nsew")
        root.grid_rowconfigure(1, weight=1) # Allow chat frame to expand vertically

        self.chat_history_text = scrolledtext.ScrolledText(
            chat_frame, width=80, height=20, wrap=tk.WORD, state=tk.DISABLED,
            bg=TEXT_AREA_BG_COLOR, fg=TEXT_AREA_FG_COLOR, font=self.chat_font,
            relief=tk.FLAT, borderwidth=1
        )
        self.chat_history_text.pack(fill=tk.BOTH, expand=True)
        self.chat_history_text.tag_config("user", background=USER_MSG_TAG_BG, foreground=FG_COLOR, font=self.chat_font, spacing1=5, spacing3=5, lmargin1=10, rmargin=10, relief=tk.RAISED, borderwidth=1)
        self.chat_history_text.tag_config("ai", background=AI_MSG_TAG_BG, foreground=TEXT_AREA_FG_COLOR, font=self.chat_font, spacing1=5, spacing3=5, lmargin1=10, rmargin=10)
        self.chat_history_text.tag_config("error", foreground="red", font=self.chat_font, spacing1=5, spacing3=5, lmargin1=10, rmargin=10)
        self.chat_history_text.tag_config("info", foreground="lightblue", font=self.chat_font, spacing1=5, spacing3=5, lmargin1=10, rmargin=10)


        # --- Input Area ---
        input_frame = tk.Frame(root, bg=BG_COLOR, padx=10, pady=10)
        input_frame.grid(row=2, column=0, sticky="ew")
        input_frame.grid_columnconfigure(0, weight=1)

        self.input_text = scrolledtext.ScrolledText(
            input_frame, width=70, height=3, wrap=tk.WORD,
            bg=INPUT_BG_COLOR, fg=FG_COLOR, insertbackground=FG_COLOR, font=self.chat_font,
            relief=tk.FLAT, borderwidth=1
        )
        self.input_text.grid(row=0, column=0, sticky="nsew", padx=(0,5))
        self.input_text.bind("<Return>", lambda event: self._handle_input_return(event))
        self.input_text.bind("<Shift-Return>", lambda event: self._handle_input_shift_return(event))


        self.submit_button = tk.Button(
            input_frame, text="Submit", command=self.submit_question,
            bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR, font=self.label_font,
            relief=tk.FLAT, activebackground="#5C6182", activeforeground=FG_COLOR, padx=10, pady=5
        )
        self.submit_button.grid(row=0, column=1, sticky="ns")

        # --- Status Bar ---
        self.status_label = tk.Label(root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W, bg=STATUS_BAR_BG_COLOR, fg=STATUS_BAR_FG_COLOR, padx=5, font=self.default_font)
        self.status_label.grid(row=3, column=0, columnspan=2, sticky="ew")

    def _handle_input_return(self, event):
        # Submit on Enter, unless Shift is held
        if event.state & 0x0001: # Shift key modifier
            return self._handle_input_shift_return(event)
        self.submit_question()
        return "break"  # Prevents the default newline insertion by Enter

    def _handle_input_shift_return(self, event):
        self.input_text.insert(tk.INSERT, "\\n")
        return "break" # Prevents the default newline (which might be different based on platform) and ensures our newline

    def _display_message(self, message, tag_name, prefix=""):
        self.chat_history_text.config(state=tk.NORMAL)
        if prefix:
            self.chat_history_text.insert(tk.END, prefix, (tag_name, "bold")) # Apply bold to prefix
            self.chat_history_text.insert(tk.END, "\\n" + message + "\\n\\n", tag_name)
        else:
            self.chat_history_text.insert(tk.END, message + "\\n\\n", tag_name)
        self.chat_history_text.see(tk.END) # Scroll to the end
        self.chat_history_text.config(state=tk.DISABLED)

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    encoded_config = f.read()
                    if encoded_config:
                        decoded_bytes = base64.b64decode(encoded_config)
                        decoded_str = decoded_bytes.decode('utf-8')
                        config_data = json.loads(decoded_str)
                        # Ensure defaults for any potentially new fields not in older configs
                        config_data.setdefault("model_name", "gpt-3.5-turbo")
                        config_data.setdefault("temperature", "0.7")
                        config_data.setdefault("max_length", "150")
                        return config_data
                    return {"model_name": "gpt-3.5-turbo", "temperature": "0.7", "max_length": "150"} # Defaults if file is empty
            except (json.JSONDecodeError, ValueError, TypeError, base64.binascii.Error):
                return {"api_key": "", "base_url": "https://api.openai.com/v1", "model_name": "gpt-3.5-turbo", "temperature": "0.7", "max_length": "150"} # Defaults on error
        return {"api_key": "", "base_url": "https://api.openai.com/v1", "model_name": "gpt-3.5-turbo", "temperature": "0.7", "max_length": "150"} # Defaults if no file

    def save_config(self, api_key, base_url, model_name, temperature, max_length):
        config = {
            "api_key": api_key,
            "base_url": base_url,
            "model_name": model_name,
            "temperature": temperature,
            "max_length": max_length
        }
        config_str = json.dumps(config)
        encoded_config = base64.b64encode(config_str.encode('utf-8')).decode('utf-8')
        with open(CONFIG_FILE, 'w') as f:
            f.write(encoded_config)

    def submit_question(self):
        self.status_label.config(text="Validating inputs...")

        api_key = self.api_key_entry.get()
        base_url = self.base_url_entry.get()
        model_name = self.model_name_entry.get()
        question = self.input_text.get("1.0", tk.END).strip() # Get from new input_text
        temperature_str = self.temperature_entry.get()
        max_length_str = self.max_length_entry.get()

        if not question:
            self.status_label.config(text="Error: Question cannot be empty.")
            self._display_message("Error: Question cannot be empty.", "error")
            return

        if not all([api_key, base_url, model_name, temperature_str, max_length_str]):
            self.status_label.config(text="Error: Config fields (API Key, Base URL, Model, Temp, Max Length) cannot be empty.")
            self._display_message("Error: Config fields (API Key, Base URL, Model, Temp, Max Length) cannot be empty.", "error")
            return

        try:
            temperature = float(temperature_str)
            if not (0.0 <= temperature <= 2.0):
                self.status_label.config(text="Error: Temperature must be between 0.0 and 2.0.")
                self._display_message("Error: Temperature must be between 0.0 and 2.0.", "error")
                return
        except ValueError:
            self.status_label.config(text="Error: Temperature must be a valid number.")
            self._display_message("Error: Temperature must be a valid number.", "error")
            return

        try:
            max_length = int(max_length_str)
            if not (1 <= max_length <= 8192): # Practical limit
                self.status_label.config(text="Error: Max Response Length must be between 1 and 8192.")
                self._display_message("Error: Max Response Length must be between 1 and 8192.", "error")
                return
        except ValueError:
            self.status_label.config(text="Error: Max Response Length must be a valid integer.")
            self._display_message("Error: Max Response Length must be a valid integer.", "error")
            return

        self.save_config(api_key, base_url, model_name, temperature_str, max_length_str)

        self._display_message(question, "user", prefix="You:")
        self.input_text.delete("1.0", tk.END) # Clear input field

        self.status_label.config(text="Submitting to AI...")
        self._display_message("...", "info") # Placeholder for AI thinking

        self.submit_button.config(state=tk.DISABLED)

        thread = threading.Thread(target=self._threaded_api_call, args=(api_key, base_url, model_name, question, temperature, max_length))
        thread.daemon = True
        thread.start()

    def _threaded_api_call(self, api_key, base_url, model_name, prompt, temperature, max_tokens):
        response = get_openai_response(api_key, base_url, model_name, prompt, temperature, max_tokens)
        self.root.after(0, self._update_gui_with_response, response)

    def _update_gui_with_response(self, response):
        # Remove the "..." placeholder before inserting the actual response
        self.chat_history_text.config(state=tk.NORMAL)
        # Find the last occurrence of "..." and delete it. This is a bit crude.
        # A more robust way would be to mark the "..." message with a specific tag and delete by tag,
        # or store a reference to it. For now, this might work if "..." is unique enough.
        pos = self.chat_history_text.search("...", "1.0", stopindex=tk.END, backwards=True, count=tk.Variable())
        if pos:
             # Ensure we're deleting the line that contains only "..." or primarily "..."
            line_start = self.chat_history_text.index(f"{pos} linestart")
            line_end = self.chat_history_text.index(f"{pos} lineend")
            line_content = self.chat_history_text.get(line_start, line_end).strip()
            if line_content == "...": # Check if the stripped line content is exactly "..."
                 # Delete the line and the preceding newline to avoid too many blank lines
                prev_char_pos = self.chat_history_text.index(f"{line_start}-1c")
                if self.chat_history_text.get(prev_char_pos, line_start) == "\\n": # If the char before line_start is a newline
                    self.chat_history_text.delete(prev_char_pos, line_end + "+1c") # Delete placeholder and its surrounding newlines
                else: # If no newline before, just delete the line and its trailing newline
                    self.chat_history_text.delete(line_start, line_end + "+1c")

        self.chat_history_text.config(state=tk.DISABLED)


        if response.startswith("Error:"):
            self._display_message(response, "error", prefix="System:")
            self.status_label.config(text="Error.")
        else:
            self._display_message(response, "ai", prefix="AI:")
            self.status_label.config(text="Done.")
        
        self.submit_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
