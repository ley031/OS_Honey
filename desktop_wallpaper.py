import tkinter as tk
from PIL import Image, ImageTk
import os
from loading_screen import show_loading_screen

class DesktopWallpaper:
    def __init__(self, root):
        self.root = root
        self.root.title("Desktop Wallpaper")
        self.root.geometry("1535x810")

        # Load the image
        self.wallpaper_image = Image.open("wallpaper.png")
        self.wallpaper_image = self.wallpaper_image.resize((1535, 810), Image.LANCZOS)
        self.wallpaper_photo = ImageTk.PhotoImage(self.wallpaper_image)

        # Create canvas for desktop wallpaper
        self.canvas = tk.Canvas(self.root, bg="white", width=1535, height=810)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Set desktop wallpaper
        self.canvas.create_image(0, 0, image=self.wallpaper_photo, anchor=tk.NW)

        # Place icons for text editor and file manager vertically on the left
        self.text_editor_icon = Image.open("icons/textEditor.png")
        self.text_editor_icon = self.text_editor_icon.resize((156, 124), Image.LANCZOS)
        self.text_editor_photo = ImageTk.PhotoImage(self.text_editor_icon)

        self.file_manager_icon = Image.open("icons/fileManager.png")
        self.file_manager_icon = self.file_manager_icon.resize((156, 124), Image.LANCZOS)
        self.file_manager_photo = ImageTk.PhotoImage(self.file_manager_icon)

        # Initial y-coordinate for the first icon
        y_start = 80

        # Gap between icons
        gap = 10

        # Create text editor icon and label
        self.canvas.create_image(810, 264.9, image=self.text_editor_photo, anchor=tk.CENTER, tags="text_editor")

        # Create file manager icon and label
        self.canvas.create_image(980, 264.9, image=self.file_manager_photo, anchor=tk.CENTER, tags="file_manager")

        # Binding events to the icons
        self.canvas.tag_bind("text_editor", "<Button-1>", self.open_text_editor)
        self.canvas.tag_bind("file_manager", "<Button-1>", self.open_file_manager)

    def open_text_editor(self, event):
        os.system("python text_editor.py")  # Assuming text_editor.py contains your text editor code

    def open_file_manager(self, event):
        os.system("explorer")  # Opens the default file explorer

def main():
    show_loading_screen()  # Show loading screen
    root = tk.Tk()
    app = DesktopWallpaper(root)
    root.overrideredirect(True)
    root.mainloop()

if __name__ == "__main__":
    main()
