import tkinter as tk
import tkinter.font as tf
import Main

window = tk.Tk()

def buildGui():
    text = "Program Started"

    window.title("HCC")
    window.iconphoto(window, tk.PhotoImage(file="C:/Users/Phoenyx/Pictures/VRChat/2022-10/VRChat_2022-10-22_16-23-08.873_1920x1080.png"))
    window.geometry("320x120")
    window.resizable(False, False)
    
    textField = tk.Text(window, width=17, height=2, state="disabled", borderwidth=0, background=window.cget("bg"), font=tf.Font(size=14))
    textField.pack()
    textField.configure(state="normal")
    textField.insert("1.0", text)
    textField.configure(state="disabled")

    start = tk.Button(window, text="Start", padx=50, pady=10, command=Main.functionToggle)
    start.pack(padx=10, pady=10)
    window.mainloop()

def killWindow():
    window.destroy()