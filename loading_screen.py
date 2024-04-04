import tkinter as tk
from PIL import Image, ImageTk

class LoadingScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Loading...")
        self.root.geometry("1535x810")
        self.root.configure(bg="black")
        
        # Load image
        self.image_original = Image.open("logo.png")  # Change "logo.png" to the path of your image
        self.image_original = self.image_original.resize((250, 250), Image.LANCZOS)  # Resize the image as needed
        self.image = ImageTk.PhotoImage(self.image_original)
        
        # Create image label
        self.image_label = tk.Label(self.root, image=self.image, bg="black")
        self.image_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)  # Place at the center, slightly above the center
        
        # Create label for "Honey OS"
        self.honey_os_label = tk.Label(self.root, text="Honey OS", font=("Questrial", 80), fg="#FFC700", bg="black", highlightbackground="black", highlightcolor="black")
        self.honey_os_label.place(relx=0.5, rely=0.55, anchor=tk.CENTER)  # Place under the image
        
        # Create label for additional text
        additional_text = "Asoy • Dico • Obrero • Silva • Tenebroso"
        self.additional_text_label = tk.Label(self.root, text=additional_text, font=("Questrial", 20), fg="#FFC700", bg="black", highlightbackground="black", highlightcolor="black")
        self.additional_text_label.place(relx=0.5, rely=0.65, anchor=tk.CENTER)  # Place under "Honey OS"
        
        # Create loading bar
        self.loading_bar = tk.Canvas(self.root, bg="gray", width=1535, height=20, bd=0, highlightthickness=0)
        self.loading_bar.pack(side=tk.BOTTOM)  # Placing at the bottom
        
        self.angle = 0  # Initial angle
        self.progress = 0
        self.load_progress()

    def load_progress(self):
        self.progress += 1
        self.loading_bar.delete("progress")  # Clear previous progress
        self.loading_bar.create_rectangle(0, 0, self.progress * (1535 / 100), 20, fill="#FFC700", tags="progress")  # Draw new progress
        
        # Rotate the image label
        self.angle += 1  # Increment angle for rotation
        rotated_image = self.image_original.rotate(self.angle, expand=True)  # Rotate the image with expanding the canvas
        self.image = ImageTk.PhotoImage(rotated_image)
        self.image_label.config(image=self.image)  # Update the image label
        
        if self.progress < 100:
            self.root.after(50, self.load_progress)
        else:
            self.root.destroy()  # Close loading screen when progress is complete

def show_loading_screen():
    root = tk.Tk()
    loading_screen = LoadingScreen(root)
    root.overrideredirect(True)
    root.mainloop()

if __name__ == "__main__":
    show_loading_screen()
