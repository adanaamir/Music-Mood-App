import tkinter as tk

def check_url():
    redirect_url = redirect_response.get("1.0", tk.END).strip()
    
    if redirect_url.startswith("https://"):
        message_label.config(text="Success!", fg="green")
    else:
        message_label.config(text="Error: Invalid URL format. Ensure the URL starts with 'https://'.", fg="red")

# Main window
window = tk.Tk()
window.geometry("600x400")
window.configure(bg="#faedd3")

# Entry widget
redirect_response = tk.Text(window, height=2, width=40)
redirect_response.place(x=200, y=500)

# Button
check_button = tk.Button(window, text="Check URL", command=check_url)
check_button.place(x=420, y=530)

# Label (Created once and updated dynamically)
message_label = tk.Label(window, text="", font=("Helvetica", 9, "bold"), bg="#faedd3")
message_label.place(x=420, y=550)

window.mainloop()
