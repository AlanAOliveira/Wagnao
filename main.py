import tkinter as tk
from tkinter import messagebox

def start_server():
    messagebox.showinfo("Start Server", "Server started successfully!")

def stop_server():
    messagebox.showinfo("Stop Server", "Server stopped successfully!")

def update():
    messagebox.showinfo("Update", "System updated successfully!")

def change_config():
    messagebox.showinfo("Change Configuration", "Configuration changed successfully!")

def help():
    messagebox.showinfo("Help", "This is a system management page. Use the buttons to manage the server.")

root = tk.Tk()
root.title("System Management")
root.geometry("300x200")

tk.Button(root, text="Start Server", command=start_server).pack(pady=5)
tk.Button(root, text="Stop Server", command=stop_server).pack(pady=5)
tk.Button(root, text="Update", command=update).pack(pady=5)
tk.Button(root, text="Change Configuration", command=change_config).pack(pady=5)
tk.Button(root, text="Help", command=help).pack(pady=5)

root.mainloop()