import tkinter as tk
from tkinter import simpledialog, Toplevel, Listbox, Button, END
import json

class PromptManager:
    def __init__(self, root, update_callback=None):  # Updated to accept update_callback
        self.root = root
        self.update_callback = update_callback  # Store the callback function
        self.prompts_file = "saved_prompts.json"
        self.prompts = self.load_prompts()
        self.listbox = None  # Initialize the Listbox variable

    def load_prompts(self):
        """Load prompts from a JSON file."""
        try:
            with open(self.prompts_file, 'r') as file:
                prompts = json.load(file)
            return [str(prompt) for prompt in prompts]
        except Exception as e:
            print(f"Failed to load prompts due to: {e}")
            return []

    def save_prompts(self):
        """Save the current prompts to a JSON file."""
        with open(self.prompts_file, 'w') as file:
            json.dump(self.prompts, file, indent=4)

    def add_prompt(self, prompt):
        """Add a new prompt to the list if it's not already present."""
        if prompt not in self.prompts:
            self.prompts.append(prompt)
            self.save_prompts()

    def remove_prompt(self, prompt):
        """Remove a prompt from the list."""
        if prompt in self.prompts:
            self.prompts.remove(prompt)
            self.save_prompts()

    def manage_prompts_dialog(self):
        """Create and manage a dialog for prompt management."""
        dialog = Toplevel(self.root)
        dialog.title("Manage Prompts")
        self.dialog_active = True  # Flag to indicate the dialog is active
        dialog.protocol("WM_DELETE_WINDOW", self.on_dialog_close)  # Handle the close event

        # Correctly initialize self.listbox as an instance variable
        self.listbox = Listbox(dialog)
        self.listbox.pack(padx=10, pady=10)

        for prompt in self.prompts:
            self.listbox.insert(END, prompt)

        Button(dialog, text="Add Prompt", command=lambda: self.add_prompt_gui()).pack(side=tk.LEFT, padx=5)
        Button(dialog, text="Remove Selected Prompt", command=lambda: self.remove_prompt_gui()).pack(side=tk.LEFT, padx=5)
        Button(dialog, text="Select", command=lambda: self.select_prompt()).pack(side=tk.RIGHT, padx=5)

        self.update_listbox = lambda: [self.listbox.delete(0, END), [self.listbox.insert(END, prompt) for prompt in self.prompts]]

    def on_dialog_close(self):
        """Handle the dialog close event."""
        self.dialog_active = False
        # Perform any necessary cleanup
    
    def add_prompt_gui(self):
        """GUI method to add a new prompt."""
        new_prompt = simpledialog.askstring("Add New Prompt", "Enter the new prompt:", parent=self.root)
        if new_prompt and new_prompt.strip() and new_prompt not in self.prompts:
            self.add_prompt(new_prompt.strip())
            self.update_listbox()  # Now correctly uses self.listbox

    def remove_prompt_gui(self):
        """GUI method to remove the selected prompt."""
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_prompt = self.listbox.get(selected_index[0])
            self.remove_prompt(selected_prompt)
            self.update_listbox()  # Now correctly uses self.listbox


    def select_prompt(self):
        """Updated method to check dialog activity before proceeding."""
        if self.listbox is not None and self.dialog_active:
            selected_index = self.listbox.curselection()
            if selected_index:
                selected_prompt = self.listbox.get(selected_index[0])
                if self.update_callback:
                    self.update_callback(selected_prompt)
                    self.root.focus_set()
        else:
            print("Dialog or Listbox is not properly initialized.")




    def get_selected_prompt(self):
        """Returns the text of the currently selected prompt."""
        if self.listbox is not None:
            try:
                selection_index = self.listbox.curselection()
                if selection_index:
                    return self.listbox.get(selection_index[0])
            except IndexError:
                pass  # Handle the case where no prompt is selected or an error occurs
        return None  # Return None if no selection is made or if listbox is not initialized

    
