import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
import threading
import socket

class CommunicationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Chat App")

        self.ip_label = tk.Label(root, text="IP Address:")
        self.ip_label.pack()
        self.ip_entry = tk.Entry(root)
        self.ip_entry.pack()

        self.port_label = tk.Label(root, text="Port:")
        self.port_label.pack()
        self.port_entry = tk.Entry(root)
        self.port_entry.pack()

        self.connect_button = tk.Button(root, text="Connect", command=self.connect)
        self.connect_button.pack()

        self.chat_area = scrolledtext.ScrolledText(root, state=tk.DISABLED)
        self.chat_area.pack(padx=10, pady=10)

        self.message_entry = tk.Entry(root)
        self.message_entry.pack(padx=10, pady=5)

        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.pack()

        self.socket = None
        self.running = False
        self.username = simpledialog.askstring("Username", "Enter your username:")

    def connect(self):
        ip = self.ip_entry.get()
        port = int(self.port_entry.get())

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((ip, port))
            self.running = True
            threading.Thread(target=self.receive_messages).start()
            self.append_message("Connected to {}:{}".format(ip, port))
        except Exception as e:
            messagebox.showerror("Error", f"Could not connect: {e}")

    def send_message(self):
        message = self.message_entry.get()
        if self.socket and self.running and message:
            try:
                full_message = f"{self.username}: {message}"
                self.socket.send(full_message.encode('utf-8'))
                self.message_entry.delete(0, tk.END)  # Clear the input field
            except Exception as e:
                self.append_message(f"Error sending message: {e}")

    def receive_messages(self):
        while self.running and self.socket:
            try:
                data = self.socket.recv(1024)
                if not data:
                    self.append_message("Connection closed by server.")
                    self.close_connection()
                    break
                message = data.decode('utf-8')
                self.append_message(message)
            except Exception as e:
                if self.running: #prevents error messages during intentional closing
                    self.append_message(f"Error receiving message: {e}")
                self.close_connection()
                break

    def append_message(self, message):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)  # Scroll to the bottom

    def close_connection(self):
        self.running = False
        if self.socket:
            try:
                self.socket.close()
            except Exception as e:
                print(f"Error closing socket: {e}")
            self.socket = None
        self.connect_button.config(state=tk.NORMAL) #re-enables the connect button
        self.append_message("Disconnected.")

    def on_closing(self):
        self.close_connection()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CommunicationApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing) #handles window closing
    root.mainloop()
