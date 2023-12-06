import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import json
import os
import sys
from PIL import Image, ImageTk

def resource_path(relative_path):
    """Get the absolute path to the resource for PyInstaller."""
    try:
        # PyInstaller creates a temp folder and stores the path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Application(tk.Frame):
    def __init__(self, master=None):
        self.null_or_zero_removed = False
        super().__init__(master, bg='#004080')  # Dark background
        self.master = master
        self.pack(fill="both", expand=True)
        self.create_widgets()
        self.json_files = []  # Initialize an empty list for JSON files
        self.file_paths = []  # Initialize an empty list for file paths
        self.deletion_log = []  # Initialize the deletion log
    def create_widgets(self):
        style = ttk.Style(root)
        font_size = 14
        style.configure("Treeview",
                        background="#004080",  # Slightly lighter navy blue for treeview items
                        foreground="#ffffff",  # White text color for contrast
                        rowheight=25,
                        fieldbackground="#003366",
                        font =('Candara',  font_size)
                        )  # Deep navy blue for the treeview field
        style.map('Treeview', background=[('selected', '#0059b3')])  # A different shade for selected item


        #style.theme_use("clam")
        # Treeview for displaying JSON structure
        self.tree = ttk.Treeview(self)
        self.tree.pack(side="left", fill="both", expand=True)

        # Scrollbar for the Treeview
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=self.scrollbar.set)


        # Delete Button
        self.delete_button = tk.Button(self, text="Delete Node", command=self.delete_node, bg='#004080', fg='#ffffff')
        self.delete_button.pack(side="top")

        # Status Bar - Repositioned for better visibility
        self.status_bar = tk.Label(self, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W, bg='#ffffff', fg='#003366')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)  # Positioned at the top for better visibility

          # IfNullDel Button
        self.ifnulldel_button = tk.Button(self, text="If Null Delete", command=self.remove_null_or_zero, bg='#004080', fg='#ffffff')
        self.ifnulldel_button.pack(side="top")
        
          #IfNullDelKey Button
        self.ifnulldelkey_button = tk.Button(self, text="IfNullDelKey", command=self.remove_null_or_zero_key, bg='#004080', fg='#ffffff')
        self.ifnulldelkey_button.pack(side="top")

        # Button to delete a specific key
        self.delete_key_button = tk.Button(self, text="Delete Specific Key", command=self.delete_specific_key, bg='#004080', fg='#ffffff')
        self.delete_key_button.pack(side="top")

        # Button to view the log
        view_log_button = tk.Button(self, text="View Deletion Log", command=self.display_log, bg='#004080', fg='#ffffff')
        view_log_button.pack(side="top")

        self.file_counter_label = tk.Label(self, text="JSON Files Loaded: 0", bg='#ffffff', fg='#004080')
        self.file_counter_label.pack(side="top")

                # Creating a menu bar
        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar, bg='#1c1c1c')

        file_menu = tk.Menu(menu_bar, tearoff=0, bg='#2c2c2c', fg='#e0e0e0')
        file_menu.add_command(label="Open", command=self.load_json_files)
        file_menu.add_command(label="Save", command=self.save_json_files)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)

        menu_bar.add_cascade(label="File", menu=file_menu)
        log_menu = tk.Menu(menu_bar, tearoff=0, bg='#2c2c2c', fg='#e0e0e0')
        log_menu.add_command(label="Save Log", command=self.save_log_to_file)
        menu_bar.add_cascade(label="Log", menu=log_menu)


    def load_json_files(self):
        directory = filedialog.askdirectory()
        if directory:
            self.json_files = []
            self.file_paths = []
            for filename in os.listdir(directory):
                if filename.endswith('.json'):
                    file_path = os.path.join(directory, filename)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        self.json_files.append(json.load(f))
                        self.file_paths.append(file_path)
            self.update_tree()
            self.file_counter_label.config(text=f"JSON Files Loaded: {len(self.json_files)}")
            self.status_bar.config(text="JSON Files Loaded")

    def update_tree(self):
        self.tree.delete(*self.tree.get_children())
        if self.json_files:
            self.insert_nodes("", self.json_files[0])

    def insert_nodes(self, parent, node):
        if isinstance(node, dict):
            for key, value in node.items():
                child = self.tree.insert(parent, "end", text=key)
                self.insert_nodes(child, value)
        elif isinstance(node, list):
            for i, value in enumerate(node):
                child = self.tree.insert(parent, "end", text=str(i))
                self.insert_nodes(child, value)
        else:
            self.tree.insert(parent, "end", text=str(node))
    def delete_node(self):
        if not self.json_files:
            messagebox.showwarning("Warning", "No JSON files loaded.")
            return

        selected = self.tree.selection()
        if selected:
            item_text = self.tree.item(selected[0])['text']
            response = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete '{item_text}' from all JSON files?")
            if response:
                key_path = self.get_key_path(selected[0])
                for json_file, file_path in zip(self.json_files, self.file_paths):
                    self.delete_key_from_path(json_file, key_path, file_path)
                self.update_tree()
                self.status_bar.config(text=f"Deleted '{item_text}' from all JSON files.")
            else:
                self.status_bar.config(text="Deletion cancelled.")




    def get_key_path(self, item):
        key_path = []
        while item:
            key_path.append(self.tree.item(item)['text'])
            item = self.tree.parent(item)
        return key_path[::-1]

    def delete_key_from_path(self, node, key_path, file_path):
        if len(key_path) == 1:
            key = key_path[0]
            if isinstance(node, dict) and key in node:
                # Log the deletion
                self.log_deletion(file_path, key_path, node[key])
                del node[key]
            elif isinstance(node, list) and key.isdigit() and int(key) < len(node):
                # Log the deletion
                self.log_deletion(file_path, key_path, node[int(key)])
                del node[int(key)]
        else:
            key = key_path[0]
            if isinstance(node, dict) and key in node:
                self.delete_key_from_path(node[key], key_path[1:], file_path)
            elif isinstance(node, list) and key.isdigit() and int(key) < len(node):
                self.delete_key_from_path(node[int(key)], key_path[1:], file_path)

        
    def save_json_files(self):
        for file_path, json_file in zip(self.file_paths, self.json_files):
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(json_file, f, ensure_ascii=False, indent=4)
        self.status_bar.config(text="JSON Files Saved")

    def remove_null_or_zero(self):
        if not self.json_files:
            messagebox.showwarning("Warning", "No JSON files loaded.")
            return

        confirmation = messagebox.askyesno("Confirm", "This will delete all 'null', '0', '0' string, and '00' string values from the loaded JSON files. Do you want to proceed?")
        if confirmation:
            for json_file, file_path in zip(self.json_files, self.file_paths):
                self.remove_null_or_zero_recursive(json_file, file_path)
            self.update_tree()
            self.status_bar.config(text="Removed null, zero, '0', and '00' string values from all JSON files.")

    def remove_null_or_zero_recursive(self, node, file_path, parent_key=None):
        if isinstance(node, dict):
            keys_to_delete = [key for key, value in node.items() if value in (0, None, "0", "00")]
            for key in keys_to_delete:
                key_to_log = (parent_key + [key]) if parent_key else [key]
                self.log_deletion(file_path, key_to_log, node[key])
                del node[key]
            for key, value in list(node.items()):
                self.remove_null_or_zero_recursive(value, file_path, parent_key=(parent_key + [key]) if parent_key else [key])

        elif isinstance(node, list):
            indices_to_delete = [i for i, value in enumerate(node) if value in (0, None, "0", "00")]
            for i in sorted(indices_to_delete, reverse=True):
                key_to_log = (parent_key + [str(i)]) if parent_key else [str(i)]
                self.log_deletion(file_path, key_to_log, node[i])
                del node[i]
            for i, value in enumerate(node):
                self.remove_null_or_zero_recursive(value, file_path, parent_key=(parent_key + [str(i)]) if parent_key else [str(i)])


    def remove_null_or_zero_key(self):
        if not self.json_files:
            messagebox.showwarning("Warning", "No JSON files loaded.")
            return

        confirmation = messagebox.askyesno("Confirm", "This will delete keys with 'null', '0', '0' string, and '00' string values from the loaded JSON files. Do you want to proceed?")
        if confirmation:
            for json_file, file_path in zip(self.json_files, self.file_paths):
                self.remove_null_or_zero_key_recursive(json_file, file_path)

            # Update the Treeview to reflect changes
            self.update_tree()
            self.status_bar.config(text="Removed keys with null, zero, '0', and '00' string values from all JSON files.")


    def remove_null_or_zero_key_recursive(self, node, file_path, parent_key=None):
        if isinstance(node, dict):
            keys_to_delete = [key for key, value in node.items() if value in (0, None, [], "", "0", "00")]
            for key in keys_to_delete:
                key_to_log = (parent_key + [key]) if parent_key else [key]
                self.log_deletion(file_path, key_to_log, node[key])
                del node[key]

            # Recursively call for nested structures, updating the dictionary as you go
            for key, value in list(node.items()):
                self.remove_null_or_zero_key_recursive(value, file_path, parent_key=(parent_key + [key]) if parent_key else [key])

        elif isinstance(node, list):
            # Handle list items
            for i in range(len(node) - 1, -1, -1):
                if node[i] in (0, None, "", [], "0", "00"):
                    key_to_log = (parent_key + [str(i)]) if parent_key else [str(i)]
                    self.log_deletion(file_path, key_to_log, node[i])
                    del node[i]
                else:
                    self.remove_null_or_zero_key_recursive(node[i], file_path, parent_key=(parent_key + [str(i)]) if parent_key else [str(i)])



    def log_deletion(self, file_path, key_path, value=None):
        # Record the deletion
        log_entry = {'file': os.path.basename(file_path), 'key_path': key_path, 'value': value}
        self.deletion_log.append(log_entry)

    def write_log_to_file(self):
        with open("deletion_log.txt", "w") as file:
            for entry in self.deletion_log:
                file.write(json.dumps(entry) + "\n")
        self.status_bar.config(text="Deletion log written to file.")

    def display_log(self):
        # Create a new top-level window
        log_window = tk.Toplevel(self)
        log_window.title("Deletion Log")
        log_window.geometry("400x300")  # Adjust the size as needed

        # Create a Text widget for log display
        log_text = tk.Text(log_window, wrap="word")
        log_text.pack(side="left", fill="both", expand=True)

        # Create a Scrollbar and attach it to the Text widget
        scrollbar = tk.Scrollbar(log_window, command=log_text.yview)
        scrollbar.pack(side="right", fill="y")
        log_text.config(yscrollcommand=scrollbar.set)

        # Format and insert log entries into the Text widget
        for count, entry in enumerate(self.deletion_log, 1):
            log_entry = f"{count}. File: {entry['file']}, Path: {' > '.join(entry['key_path'])}, Deleted Value: {entry['value']}\n"
            log_text.insert("end", log_entry)

        # Make the Text widget read-only
        log_text.config(state="disabled")


    def save_log_to_file(self):
        if not self.file_paths:
            self.status_bar.config(text="No directory selected. Unable to save log.")
            return

        directory = os.path.dirname(self.file_paths[0])
        log_file_path = os.path.join(directory, "deletion_log.txt")

        with open(log_file_path, "w", encoding='utf-8') as file:
            for count, entry in enumerate(self.deletion_log, 1):
                log_entry = f"{count}. File: {entry['file']}, Path: {' > '.join(entry['key_path'])}, Deleted Value: {entry['value']}\n"
                file.write(log_entry)

        self.status_bar.config(text=f"Deletion log saved to {log_file_path}.")

    def delete_specific_key(self):
        if not self.json_files:
            messagebox.showwarning("Warning", "No JSON files loaded.")
            return

        key_to_delete = simpledialog.askstring("Input", "Enter key to delete", parent=self.master)
        if key_to_delete:
            confirmation = messagebox.askyesno("Confirm", f"Are you sure you want to delete the key '{key_to_delete}' from all JSON files?")
            if confirmation:
                key_found = False
                for json_file, file_path in zip(self.json_files, self.file_paths):
                    if self.delete_key_recursive(json_file, key_to_delete, file_path):
                        key_found = True

                if key_found:
                    self.update_tree()
                    self.status_bar.config(text=f"Deleted key '{key_to_delete}' from all JSON files.")
                else:
                    messagebox.showinfo("Info", f"No match was found for key '{key_to_delete}'.")
 


    def delete_key_recursive(self, node, key_to_delete, file_path, parent_key=None):
        key_found = False
        if isinstance(node, dict):
            if key_to_delete in node:
                # Log the deletion
                key_to_log = (parent_key + [key_to_delete]) if parent_key else [key_to_delete]
                self.log_deletion(file_path, key_to_log, node[key_to_delete])
                del node[key_to_delete]
                key_found = True

            for key, value in list(node.items()):
                if self.delete_key_recursive(value, key_to_delete, file_path, parent_key=(parent_key + [key]) if parent_key else [key]):
                    key_found = True

        elif isinstance(node, list):
            for i, value in enumerate(node):
                if self.delete_key_recursive(value, key_to_delete, file_path, parent_key=(parent_key + [str(i)]) if parent_key else [str(i)]):
                    key_found = True

        return key_found

root = tk.Tk()
root.title("Bulk JSON Editor")
root.geometry("800x600")
logo_path = resource_path("Bulk_JSON_Editor_Logo.ico")
logo_image = Image.open(logo_path)
logo_image = logo_image.resize((100, 100), Image.Resampling.LANCZOS)  # Resize to 100x100 or your preferred size


root.iconphoto(False, ImageTk.PhotoImage(logo_image))
logo_photoimage = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(root, image=logo_photoimage)
logo_label.pack()

app = Application(master=root)
app.mainloop()
