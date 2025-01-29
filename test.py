import tkinter as tk
from PIL import Image, ImageTk  # Make sure to install Pillow library

# Create the main window
root = tk.Tk()
root.title("Icon Example")

# Set the icon for the main window
icon = ImageTk.PhotoImage(file="icon.png")
root.iconphoto(False, icon)

# Create a label to display some text
label = tk.Label(root, text="This is a window with an icon")
label.pack(pady=20)

# Start the main event loop
root.mainloop()