import tkinter as tk

window = tk.Tk()
window.title("MY GUI")

top_frame = tk.Frame(window).pack()
bottomFrame = tk.Frame(window).pack(side="bottom")

btn1 = tk.Button(bottomFrame, text="BUTTON 1", fg="red").pack()
btn2 = tk.Button(top_frame, text="BUTTON 2", fg="pink").pack()
btn3 = tk.Button(bottomFrame, text="BUTTON 3", fg="green").pack()
btn4 = tk.Button(top_frame, text="BUTTON 4", fg="blue").pack()

window.mainloop()