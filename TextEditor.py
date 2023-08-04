import tkinter as tk
from tkinter import filedialog, messagebox
from VoiceCapture import *

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Cross-Platform Text Editor")
        self.text_area = tk.Text(root, wrap="word", undo=True)
        self.text_area.pack(expand="yes", fill="both")
        self.canvas = tk.Canvas(root, width=200, height=200)
        self.canvas.pack()
        self.create_menu()
        self.vc = VoiceCapture(self.text_area, self.canvas)
        # Bind the "WM_DELETE_WINDOW" event to the on_closing function
        root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As...", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.text_area.edit_undo)
        edit_menu.add_command(label="Redo", command=self.text_area.edit_redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self.cut)
        edit_menu.add_command(label="Copy", command=self.copy)
        edit_menu.add_command(label="Paste", command=self.paste)
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", command=self.select_all)

        voice_menu = tk.Menu(menubar, tearoff=0)
        voice_menu.add_command(label="Start", command=self.start_voice)
        voice_menu.add_command(label="Stop", command=self.stop_voice)

        audio_menu = tk.Menu(menubar, tearoff=0)
        audio_menu.add_command(label="On", command=self.audioDisplay)
        audio_menu.add_command(label="Off", command=self.audioDisplay)

        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        menubar.add_cascade(label="Voice", menu=voice_menu)
        menubar.add_cascade(label="Audio", menu=audio_menu)

        self.root.config(menu=menubar)

    def audioDisplay(self):
        print("Audio Display ")
        
    def new_file(self):
        self.text_area.delete("1.0", tk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert(tk.END, file.read())

    def save_file(self):
        if not self.text_area.get("1.0", tk.END).strip():
            messagebox.showinfo("Warning", "Cannot save an empty file.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_area.get("1.0", tk.END))

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_area.get("1.0", tk.END))

    def start_voice(self):
        print("Voice Recording Start")
        #textfield = self.text_area
        self.vc.start_action()
        #voiceCap = vc()
        #voiceCap.startRecording()
        #text = self.text_area.get("1.0", tk.END)
        

    def stop_voice(self):
        print("Voice Recording Stop")
        if(self.vc.isRunning == True):
            self.vc.stop_action()
        
        
    def on_closing(self):
        print("Window is closing...")
        self.stop_voice()
        # Additional cleanup or actions before closing (if needed)        
        root.withdraw()



    def cut(self):
        self.text_area.event_generate("<<Cut>>")

    def copy(self):
        self.text_area.event_generate("<<Copy>>")

    def paste(self):
        self.text_area.event_generate("<<Paste>>")

    def select_all(self):
        self.text_area.tag_add("sel", "1.0", tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    text_editor = TextEditor(root)
    root.mainloop()
