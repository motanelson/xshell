import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import subprocess
global root
frames =None

class XShellApp:
    def __init__(self, root):
        self.root = root
        self.root.title("XShell Viewer")
        self.canvas = tk.Canvas(root, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.rectangles = []
        self.commands = []

        # Load the Xshell file
        self.load_button = tk.Button(root, text="Load .Xshell File", command=self.load_xshell_file)
        self.load_button.pack(side=tk.BOTTOM, pady=10)

    def load_xshell_file(self):
        xshell_path = filedialog.askopenfilename(filetypes=[("XShell Files", "*.Xshell")])
        if not xshell_path:
            return

        try:
            with open(xshell_path, "r") as file:
                lines = file.readlines()

            if len(lines) < 1:
                messagebox.showerror("Error", "Invalid .Xshell file format!")
                return

            # Load the image
            image_path = lines[0].strip()
            if not os.path.exists(image_path):
                messagebox.showerror("Error", f"Image file not found: {image_path}")
                return

            self.load_image(image_path)

            # Parse rectangles and commands
            self.rectangles.clear()
            self.commands.clear()

            for line in lines[1:]:
                parts = line.strip().split(",")
                if len(parts) != 5:
                    continue

                x, y, width, height, command = parts
                x, y, width, height = map(int, (x, y, width, height))
                self.rectangles.append((x, y, width, height))
                self.commands.append(command)

            

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load .Xshell file: {e}")

    def load_image(self, image_path):
        self.image = Image.open(image_path)
        self.photo = ImageTk.PhotoImage(self.image)
        img=self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        self.canvas.config(width=self.image.width, height=self.image.height)
        self.canvas.tag_bind(img, "<Button-1>", self.execute_command)

    

    def execute_command(self, event):
        print(event)
        #command = self.commands[idx]
        idx=0;
        for n in self.rectangles:
            if event.x>n[0] and event.x<n[0]+n[2] and event.y>n[1] and event.y<n[1]+n[3]:
                
                try:
                     subprocess.run(self.commands[idx], shell=True)
            
                except Exception as e:
                     messagebox.showerror("Error", f"Failed to execute command: {e}")
            idx+=1
       


if __name__ == "__main__":
    root = tk.Tk()
    app = XShellApp(root)
    root.mainloop()
