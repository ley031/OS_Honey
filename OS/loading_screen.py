import tkinter as tk

class LoadingScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Loading...")
        self.root.geometry("1535x810")
        self.root.configure(bg="black")
        
        # Create loading label with white text
        self.loading_label = tk.Label(self.root, text="Loading...", font=("Helvetica", 16), fg="white", bg="black")
        self.loading_label.pack(pady=20)
        
        # Create loading bar
        self.loading_bar = tk.Canvas(self.root, bg="gray", width=250, height=20, bd=0, highlightthickness=0)
        self.loading_bar.pack()
        
        self.progress = 0
        self.load_progress()

    def load_progress(self):
        self.progress += 1
        self.loading_bar.create_rectangle(0, 0, self.progress * 2.5, 20, fill="yellow")  # White loading bar
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
