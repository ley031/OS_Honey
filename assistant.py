import speech_recognition as sr
from gtts import gTTS
import winsound
from pydub import AudioSegment
import pyautogui
import os
from text_editor import TextEditor  
import tkinter as tk
import threading

def open_file_manager():
    os.system("explorer")  # Opens the default file explorer

def close_file_manager():
    # You can't directly close the file manager (explorer) using Python
    # It's up to the user to manually close it
    pass
def open_text_editor():
    root = tk.Tk()
    app = TextEditor(root)
    root.mainloop()

def close_text_editor(root):
    root.destroy()
    respond("Text editor closed.")
    root.quit()  # Quit the tkinter main loop

def listen_for_command():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening for commands...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        print("Could not understand audio. Please try again.")
        return None
    except sr.RequestError:
        print("Unable to access the Google Speech Recognition API.")
        return None

def respond(response_text):
    print(response_text)
    tts = gTTS(text=response_text, lang='en')
    tts.save("response.mp3")
    sound = AudioSegment.from_mp3("response.mp3")
    sound.export("response.wav", format="wav")
    winsound.PlaySound("response.wav", winsound.SND_FILENAME)
    # os.system("afplay response.mp3") for non-windows

tasks = []
listeningToTask = False

def voice():
    text_editor_instance = None  # Initialize text_editor_instance to None
    while True:
        command = listen_for_command()

        triggerKeyword = "please"

        if command and triggerKeyword in command:
            if "work" in command:
                respond("I'm working.")
            elif "open text editor" in command:
                respond("Opening text editor.")
                if not text_editor_instance:  # If text_editor_instance is None, create a new TextEditor instance
                    threading.Thread(target=open_text_editor).start()
                    text_editor_instance = True  # Set text_editor_instance to True to indicate the text editor is open
                else:
                    respond("Text editor is already open.")
            elif "close text editor" in command:
                respond("Closing text editor.")
                if text_editor_instance:  # If text_editor_instance is True, close the text editor
                    threading.Thread(target=close_text_editor, args=(tk._default_root,)).start()
                    text_editor_instance = None  # Set text_editor_instance back to None to indicate the text editor is closed
                else:
                    respond("Text editor is already closed.")
            elif "open file manager" in command:
                respond("Opening file manager.")
                open_file_manager()

            elif "new file" in command:
                respond("Creating a new file.")
            elif "open file" in command:
                respond("Opening a file.")
            elif "save file" in command:
                respond("Saving file.")
            elif "close current tab" in command:
                respond("Closing current tab.")
            elif "take a screenshot" in command:
                pyautogui.screenshot("screenshot.png")
                respond("I took a screenshot for you.")
            elif "exit" in command:
                respond("Goodbye!")
                break
            else:
                respond("Sorry, I'm not sure how to handle that command.")

if __name__ == "__main__":
    voice()

