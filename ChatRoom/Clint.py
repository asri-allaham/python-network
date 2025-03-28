import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

def GUI(client_socket):
    #window and GUI systme...
    window = tk.Tk()
    window.title("Chat Client")
    window.geometry("600x500")
    window.config(bg="#2b2b2b")

    text_widget = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=60, height=18, bg="#1e1e1e", fg="#ffffff", font=("Arial", 12))
    text_widget.pack(padx=10, pady=10)
    text_widget.config(state=tk.DISABLED)

    entry_frame = tk.Frame(window, bg="#2b2b2b")
    entry_frame.pack(pady=5)

    tk.Label(entry_frame, text="Enter Message:", bg="#2b2b2b", fg="#ffffff", font=("Arial", 12)).grid(row=0, column=0, sticky="w")
    message_entry = tk.Entry(entry_frame, width=45, font=("Arial", 12), bg="#3c3f41", fg="#ffffff", insertbackground="#ffffff")
    message_entry.grid(row=1, column=0, padx=(0, 10), ipady=5)

    # Send button
    send_button = tk.Button(entry_frame, text="Send", width=10, bg="#4caf50", fg="#ffffff", font=("Arial", 12, "bold"),
                            activebackground="#45a049", activeforeground="#ffffff", cursor="hand2",
                            command=lambda: send_message(client_socket, message_entry, text_widget))#On click will call send_message system..
    send_button.grid(row=1, column=1)

    return window, text_widget

def receive_messages(client_socket, text_widget):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                text_widget.config(state=tk.NORMAL)
                text_widget.insert(tk.END, message + '\n')
                text_widget.yview(tk.END)
                text_widget.config(state=tk.DISABLED)
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

def send_message(client_socket, message_entry, text_widget):
    message = message_entry.get().strip()
    if message:
        text_widget.config(state=tk.NORMAL)
        text_widget.insert(tk.END, f"You: {message}\n")
        text_widget.yview(tk.END)
        text_widget.config(state=tk.DISABLED)

        try:
            client_socket.send(message.encode())
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send message: {e}")
        
        message_entry.delete(0, tk.END)


def on_closing(client_socket):
    try:
        client_socket.close()
    except:
        pass
    window.destroy()

def start_client():
    global window
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(('xx.xxx.xxx', 12345))  
    
    except Exception as e:
        messagebox.showerror("Connection Error", f"Unable to connect to server: {e}")
        return

    window, text_widget = GUI(client_socket)

    window.protocol("WM_DELETE_WINDOW", lambda: on_closing(client_socket))

    threading.Thread(target=receive_messages, args=(client_socket, text_widget), daemon=True).start()

    window.mainloop()

if __name__ == "__main__":
    start_client()
