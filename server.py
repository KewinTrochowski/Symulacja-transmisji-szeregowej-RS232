import tkinter as tk
import socket
import threading

def decode(bit_string):
    chars = []
    for i in range(0, len(bit_string), 11):
        byte = bit_string[i+1:i+9]
        ascii_value = int(byte[::-1], 2)
        chars.append(chr(ascii_value))
    return ''.join(chars)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 12345))
    server_socket.listen(1)
    while True:
        client_socket, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

def handle_client(client_socket):
    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break
        decoded_message = decode(data)
        result.insert(tk.END, f"Received: {decoded_message}\n")
    client_socket.close()


root = tk.Tk()
root.title("Server")

result = tk.Text(root, height=20, width=50)
result.pack()

# Start server thread
server_thread = threading.Thread(target=start_server)
server_thread.start()

root.mainloop()
