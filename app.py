import tkinter as tk
from tkinter import scrolledtext
import threading
from openai_client import get_openai_response

class App:
    def __init__(self, root):
        self.root = root
        root.title("OpenAI API Client")

        # API Key
        tk.Label(root, text="API Key:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.api_key_entry = tk.Entry(root, width=50, show='*')
        self.api_key_entry.grid(row=0, column=1, padx=5, pady=5)

        # Base URL
        tk.Label(root, text="Base URL:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.base_url_entry = tk.Entry(root, width=50)
        self.base_url_entry.grid(row=1, column=1, padx=5, pady=5)
        self.base_url_entry.insert(0, "https://api.openai.com/v1") # Default value

        # Model Name
        tk.Label(root, text="Model Name:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.model_name_entry = tk.Entry(root, width=50)
        self.model_name_entry.grid(row=2, column=1, padx=5, pady=5)
        self.model_name_entry.insert(0, "gpt-3.5-turbo") # Default value

        # Temperature
        tk.Label(root, text="Temperature:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.temperature_entry = tk.Entry(root, width=10)
        self.temperature_entry.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        self.temperature_entry.insert(0, "0.7") # Default value

        # Max Response Length
        tk.Label(root, text="Max Response Length:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.max_length_entry = tk.Entry(root, width=10)
        self.max_length_entry.grid(row=4, column=1, sticky="w", padx=5, pady=5)
        self.max_length_entry.insert(0, "150") # Default value

        # User Question
        tk.Label(root, text="Your Question:").grid(row=5, column=0, sticky="nw", padx=5, pady=5)
        self.question_entry = scrolledtext.ScrolledText(root, width=60, height=5, wrap=tk.WORD)
        self.question_entry.grid(row=5, column=1, padx=5, pady=5)

        # AI Answer
        tk.Label(root, text="AI's Answer:").grid(row=6, column=0, sticky="nw", padx=5, pady=5)
        self.answer_text = scrolledtext.ScrolledText(root, width=60, height=10, wrap=tk.WORD, state=tk.DISABLED)
        self.answer_text.grid(row=6, column=1, padx=5, pady=5)

        # Submit Button
        self.submit_button = tk.Button(root, text="Submit", command=self.submit_question)
        self.submit_button.grid(row=7, column=1, pady=10, padx=5, sticky="e")

        # Status Bar
        self.status_label = tk.Label(root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.grid(row=8, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

    def submit_question(self):
        self.status_label.config(text="Validating inputs...")

        api_key = self.api_key_entry.get()
        base_url = self.base_url_entry.get()
        model_name = self.model_name_entry.get()
        question = self.question_entry.get("1.0", tk.END).strip()
        temperature_str = self.temperature_entry.get()
        max_length_str = self.max_length_entry.get()

        if not all([api_key, base_url, model_name, question]):
            self.status_label.config(text="Error: API Key, Base URL, Model Name, and Question cannot be empty.")
            return

        try:
            temperature = float(temperature_str)
            if not (0.0 <= temperature <= 2.0):
                self.status_label.config(text="Error: Temperature must be between 0.0 and 2.0.")
                return
        except ValueError:
            self.status_label.config(text="Error: Temperature must be a valid number.")
            return

        try:
            max_length = int(max_length_str)
            # Assuming a reasonable range for max_tokens, e.g. gpt-3.5-turbo-instruct has 4096
            # For chat models, it's more about total tokens in context, but max_tokens for response is still relevant.
            # Let's use 1 to 8192 as a general practical limit.
            if not (1 <= max_length <= 8192):
                self.status_label.config(text="Error: Max Response Length must be between 1 and 8192.")
                return
        except ValueError:
            self.status_label.config(text="Error: Max Response Length must be a valid integer.")
            return

        self.status_label.config(text="Submitting question...")
        self.submit_button.config(state=tk.DISABLED) # Disable button during API call
        self.answer_text.config(state=tk.NORMAL)
        self.answer_text.delete(1.0, tk.END)
        self.answer_text.config(state=tk.DISABLED)

        # Run API call in a separate thread to avoid freezing the GUI
        thread = threading.Thread(target=self._threaded_api_call, args=(api_key, base_url, model_name, question, temperature, max_length))
        thread.daemon = True # Allow main program to exit even if threads are still running
        thread.start()

    def _threaded_api_call(self, api_key, base_url, model_name, prompt, temperature, max_tokens):
        response = get_openai_response(api_key, base_url, model_name, prompt, temperature, max_tokens)
        # Schedule GUI update on the main thread
        self.root.after(0, self._update_gui_with_response, response)

    def _update_gui_with_response(self, response):
        self.answer_text.config(state=tk.NORMAL)
        self.answer_text.delete(1.0, tk.END)
        self.answer_text.insert(tk.INSERT, response)
        self.answer_text.config(state=tk.DISABLED)
        self.submit_button.config(state=tk.NORMAL) # Re-enable button

        if response.startswith("Error:"):
            self.status_label.config(text=response)
        else:
            self.status_label.config(text="Done.")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
