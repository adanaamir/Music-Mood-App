import tkinter as tk
from tkinter import messagebox

def recommend_music(mood):
    recommendations = {
        "Happy": ["Happy - Pharrell Williams", "Can't Stop the Feeling - Justin Timberlake"],
        "Sad": ["Someone Like You - Adele", "Fix You - Coldplay"],
        "Relaxed": ["Weightless - Marconi Union", "Breezeblocks - Alt-J"],
        "Energetic": ["Eye of the Tiger - Survivor", "Uptown Funk - Bruno Mars"]
    }
    return recommendations.get(mood, ["No recommendations available"])

def show_recommendations(mood):
    songs = recommend_music(mood)
    messagebox.showinfo(f"{mood} Playlist", "\n".join(songs))

# Create the main window
root = tk.Tk()
root.title("Music Mood App")
root.geometry("300x200")

# Add a label
label = tk.Label(root, text="Select your mood:", font=("Arial", 14))
label.pack(pady=10)

# Add buttons for moods
moods = ["Happy", "Sad", "Relaxed", "Energetic"]
for mood in moods:
    button = tk.Button(root, text=mood, font=("Arial", 12), command=lambda m=mood: show_recommendations(m))
    button.pack(pady=5)

# Run the main loop
root.mainloop()
