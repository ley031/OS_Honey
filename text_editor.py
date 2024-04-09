import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import os

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, text=self.text, background="#ffffe0", relief="solid", borderwidth=1)
        label.pack()

    def hide_tooltip(self, event=None):
        if hasattr(self, "tooltip"):
            self.tooltip.destroy()

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Text Editor")

        # Create a style
        self.style = ttk.Style()
        self.style.theme_create("my_theme", parent="alt", settings={
            "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}},
            "TNotebook.Tab": {"configure": {"padding": [10, 5], "background": "#FFFF00"},
                              "map": {"background": [("selected", "#FFFF00")]}},
        })
        self.style.theme_use("my_theme")

        # Configure rows and columns to expand
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Create a frame to contain the buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.grid(row=0, column=0, sticky="ns")

        # Create icons with adjusted size
        self.icons = {
            "New": tk.PhotoImage(file="icons/new.png").subsample(13, 13),
            "Open": tk.PhotoImage(file="icons/open.png").subsample(13, 13),
            "Save": tk.PhotoImage(file="icons/save.png").subsample(13, 13),
            "SaveAs": tk.PhotoImage(file="icons/saveas.png").subsample(13, 13),
            "Cut": tk.PhotoImage(file="icons/cut.png").subsample(13, 13),
            "Copy": tk.PhotoImage(file="icons/copy.png").subsample(13, 13),
            "Paste": tk.PhotoImage(file="icons/paste.png").subsample(13, 13),
            "Undo": tk.PhotoImage(file="icons/undo.png").subsample(13, 13),
            "Redo": tk.PhotoImage(file="icons/redo.png").subsample(13, 13),
            "Close": tk.PhotoImage(file="icons/close.png").subsample(13, 13),
        }

        # Create buttons placed vertically at the left
        self.buttons = {
            "New": self.create_button("New", self.new_file, 0),
            "Open": self.create_button("Open", self.open_file, 1),
            "Save": self.create_button("Save", self.save_file, 2),
            "SaveAs": self.create_button("SaveAs", self.save_as_file, 3),
            "Cut": self.create_button("Cut", self.cut_text, 4),
            "Copy": self.create_button("Copy", self.copy_text, 5),
            "Paste": self.create_button("Paste", self.paste_text, 6),
            "Undo": self.create_button("Undo", self.undo, 7),
            "Redo": self.create_button("Redo", self.redo, 8),
            "Close": self.create_button("Close", self.close_tab, 9),  # Close button
        }

        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=0, column=1, sticky="nsew")

        self.notebook.bind("<Control-w>", self.close_tab)

        self.add_tab()

    def create_button(self, name, command, row):
        button = tk.Button(self.button_frame, image=self.icons[name], command=command, bg="black")
        button.grid(row=row, column=0, pady=0)
        ToolTip(button, name)
        return button

    def add_tab(self, filename="Untitled"):
        text_widget = tk.Text(self.notebook, undo=True, bg="black", fg="yellow")
        text_widget.pack(expand=True, fill='both')
        text_widget.filename = filename  # Store filename as an attribute of the Text widget
        self.notebook.add(text_widget, text=filename)



    def new_file(self, event=None):
        self.add_tab()

    def open_file(self, event=None):
        file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file:
            with open(file, "r") as f:
                text = f.read()
                
            text_widget = tk.Text(self.notebook, undo=True, bg="black", fg="yellow")
            text_widget.insert("1.0", text)
            text_widget.pack(expand=True, fill='both')
            text_widget.filename = f.name
            self.notebook.add(text_widget, text=file)

    def save_file(self, event=None):
        selected_tab = self.notebook.select()
        text_widget = self.notebook.nametowidget(selected_tab)
        current_tab = self.notebook.tab(text_widget)
        filename = self.notebook.tab(current_tab, "text")

        if filename == "Untitled":
            self.save_as_file()
        else:
            with open(filename, "w") as f:
                f.write(text_widget.get("1.0", tk.END))

    def save_as_file(self, event=None):
        selected_tab = self.notebook.select()
        text_widget = self.notebook.nametowidget(selected_tab)
        file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file:
            filename = file
            with open(filename, "w") as f:
                f.write(text_widget.get("1.0", tk.END))
            self.notebook.tab(text_widget, text=filename)

    def cut_text(self):
        selected_tab = self.notebook.select()
        text_widget = self.notebook.nametowidget(selected_tab)
        text_widget.event_generate("<<Cut>>")

    def copy_text(self):
        selected_tab = self.notebook.select()
        text_widget = self.notebook.nametowidget(selected_tab)
        text_widget.event_generate("<<Copy>>")

    def paste_text(self):
        selected_tab = self.notebook.select()
        text_widget = self.notebook.nametowidget(selected_tab)
        text_widget.event_generate("<<Paste>>")

    def undo(self):
        selected_tab = self.notebook.select()
        text_widget = self.notebook.nametowidget(selected_tab)
        text_widget.event_generate("<<Undo>>")

    def redo(self):
        selected_tab = self.notebook.select()
        text_widget = self.notebook.nametowidget(selected_tab)
        text_widget.event_generate("<<Redo>>")

    def close_tab(self, event=None):
        selected_tab = self.notebook.select()
        text_widget = self.notebook.nametowidget(selected_tab)
        filename = text_widget.filename  # Get filename from the attribute of the Text widget

        text = text_widget.get("1.0", tk.END).strip()  # Get text and remove trailing whitespaces

        if filename != "Untitled" and (text or os.path.exists(filename)):
            with open(filename, "r") as f:
                if f.read().strip() != text:  # Compare stripped text
                    confirm = messagebox.askyesnocancel("Unsaved Changes", f"Do you want to save changes to {filename} before closing?")
                    if confirm:
                        self.save_file()
                    elif confirm is None:
                        return
        self.notebook.forget(selected_tab)

        # Check if there are any tabs left, if not, close the application
        if not self.notebook.tabs():
            self.root.quit()
    def open_editor(self):
        print("Opening text editor")  # Add a debug message
        self.root.deiconify()  # Show the text editor window if it was minimized or hidden

    def close_editor(self):
        print("Closing text editor")  # Add a debug message
        self.root.withdraw()  # Hide the text editor window


root = tk.Tk()
app = TextEditor(root)
root.mainloop()