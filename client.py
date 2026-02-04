import socket
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext

# ---------- Connect to server ----------
HOST = '127.0.0.1'
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# ---------- GUI ----------
root = tk.Tk()
root.title("Chat Client")
root.geometry("400x500")

messages_frame = tk.Frame(root)
msg_list = scrolledtext.ScrolledText(messages_frame, wrap='word', state='disabled')
msg_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
messages_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

entry_field = tk.Entry(root)
entry_field.pack(fill=tk.X, padx=10, pady=5)

def send_message():
    message = entry_field.get()
    if message:
        client.send(message.encode('utf-8'))
        entry_field.delete(0, tk.END)

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(pady=5)

# ---------- Receive messages ----------
def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                msg_list.config(state='normal')
                msg_list.insert(tk.END, message + '\n')  # Shows "Nickname: message"
                msg_list.yview(tk.END)
                msg_list.config(state='disabled')
        except:
            print("An error occurred!")
            client.close()
            break

# ---------- Ask for nickname ----------
nickname = simpledialog.askstring("Nickname", "Choose your nickname", parent=root)
if not nickname:
    messagebox.showerror("Error", "You must enter a nickname")
    root.destroy()
else:
    threading.Thread(target=receive_messages).start()
    root.mainloop()
