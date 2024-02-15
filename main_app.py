# main_app.py
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, Scrollbar, Text, Listbox, END, Frame, Button, Label
import os
import whisper
from openai import OpenAI
from prompt_manager import PromptManager  # Ensure this import matches your file structure
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client with your API key
api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    api_key = simpledialog.askstring("API Key", "Enter your OpenAI API Key:")
    with open(".env", "w") as file:
        file.write(f"OPENAI_API_KEY={api_key}")

load_dotenv()  # Reload to update environment variables within the application
client = OpenAI(api_key=api_key)

# Initialize OpenAI client with your API key


# Function to update the UI with the selected prompt from PromptManager
def update_selected_prompt(prompt):
    selected_prompt_var.set(prompt)  # Updates the variable holding the selected prompt
    selected_prompt_label.config(text=f"Selected Prompt: {prompt}")  # Update label text to show selected prompt

def select_file_and_process():
    filename = filedialog.askopenfilename(title="Select Audio File", filetypes=[("Audio Files", "*.mp3 *.wav *.m4a *.mp4 *.mpeg *.mpga *.webm")])
    if not filename:
        update_status("No file selected.")
        return
    update_status("Transcribing... Please wait.")
    transcription = transcribe_audio(filename)
    load_transcription_into_gui(transcription)
    update_status("Transcription completed.")

def send_to_chatgpt():
    transcription = transcription_text.get("1.0", "end").strip()
    selected_prompt = selected_prompt_var.get()
    if not transcription or selected_prompt == "Select a prompt":
        messagebox.showwarning("Warning", "Please load text and select a valid prompt before sending to ChatGPT.")
        return
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"{selected_prompt}\n\n{transcription}"}
            ]
        )
        # Adjusted line to correctly access the content of the message
        chat_response = response.choices[0].message.content
        transcription_text.insert("end", "\n\nChatGPT Response:\n" + chat_response)
        update_status("Response from ChatGPT received.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to get response from ChatGPT: {str(e)}")


def transcribe_audio(file_path):
    model = whisper.load_model("base")
    result = model.transcribe(file_path)
    return result["text"]

# Adjust the load_folder function for default behavior
def load_folder():
    default_folder = os.path.join(os.getcwd(), "audio")
    if not os.path.exists(default_folder):
        os.makedirs(default_folder)
    folder_path = filedialog.askdirectory(initialdir=default_folder)
    if not folder_path:
        update_status("No folder selected.")
        return
    current_folder.set(folder_path)
    update_file_list(folder_path)

def update_file_list(folder_path):
    txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    file_list.delete(0, END)
    for file in txt_files:
        file_list.insert(END, file)
    update_status(f"Loaded .txt files from {folder_path}")

def load_transcription_from_file():
    try:
        selected_index = file_list.curselection()[0]
        selected_file = file_list.get(selected_index)
        full_path = os.path.join(current_folder.get(), selected_file)
        with open(full_path, 'r', encoding='utf-8') as file:
            transcription = file.read()
            load_transcription_into_gui(transcription)
            update_status(f"Displayed contents of {selected_file}")
    except IndexError:
        update_status("No file selected from the list.")

def save_transcription():
    transcription = transcription_text.get(1.0, END)
    filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if filename:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(transcription)
        update_status(f"Transcription saved as {os.path.basename(filename)}")

def load_transcription_into_gui(transcription):
    transcription_text.delete(1.0, END)
    transcription_text.insert(END, transcription)

def update_status(message):
    status_label.config(text=message)

# GUI Setup
root = tk.Tk()
root.title("Audio Transcription with Whisper and ChatGPT")
root.geometry("800x600")

current_folder = tk.StringVar(root)  # Define this variable for folder path tracking

frame_top = Frame(root)
frame_top.pack(fill='x', padx=10, pady=5)

frame_bottom = Frame(root)
frame_bottom.pack(fill='both', expand=True, padx=10, pady=5)

selected_prompt_var = tk.StringVar(root)
selected_prompt_var.set("Select a prompt")  # Default prompt selection

# Instantiate PromptManager with a callback to update selected prompt display
prompt_manager = PromptManager(root, update_selected_prompt)  # Pass the callback function here

# Adjust Button to open the prompt management dialog - Now correctly placed in frame_bottom
manage_prompts_button = Button(frame_bottom, text="Manage Prompts", command=prompt_manager.manage_prompts_dialog)
manage_prompts_button.pack(side='left', padx=5, pady=10)

# Correctly place the "Send to ChatGPT" button - Ensure it's only packed once
send_to_chatgpt_button = Button(frame_bottom, text="Send to ChatGPT", command=send_to_chatgpt)
send_to_chatgpt_button.pack(side='left', padx=5, pady=10)

# Label to display the selected prompt
selected_prompt_label = Label(root, text="Selected Prompt: None")
selected_prompt_label.pack(pady=(5, 10))



# Buttons for transcribing, sending to ChatGPT, loading a folder, and saving transcription
process_button = Button(frame_top, text="Select Audio File and Transcribe", command=select_file_and_process)
process_button.pack(side='left', padx=(0, 5))



load_folder_button = Button(frame_top, text="Load Folder", command=load_folder)
load_folder_button.pack(side='left', padx=5)

save_as_button = Button(frame_top, text="Save As", command=save_transcription)
save_as_button.pack(side='left', padx=(5, 0))

# Status label to display current action status
status_label = Label(frame_top, text="Select an audio file or load a folder.")
status_label.pack(side='left', padx=(10, 0))

# Listbox to display .txt files from the loaded folder
file_list = Listbox(frame_bottom, height=10)
file_list.pack(side='left', fill='y', padx=(0, 5))
scrollbar = Scrollbar(frame_bottom, orient='vertical', command=file_list.yview)
scrollbar.pack(side='left', fill='y')
file_list.config(yscrollcommand=scrollbar.set)

# Text widget to display and edit the transcription or ChatGPT responses
transcription_text = Text(frame_bottom, wrap='word')
transcription_text.pack(side='left', fill='both', expand=True)
scrollbar_text = Scrollbar(frame_bottom, orient='vertical', command=transcription_text.yview)
scrollbar_text.pack(side='left', fill='y')
transcription_text.config(yscrollcommand=scrollbar_text.set)

# Bind the Listbox selection event to load the selected transcription into the Text widget
file_list.bind('<<ListboxSelect>>', lambda event: load_transcription_from_file())



root.mainloop()
