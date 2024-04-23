import tkinter as tk
import socket

def encode(text):
    encoded = ""
    for char in text:
        ascii_value = ord(char)
        bit_string = '0' + format(ascii_value, '08b')[::-1] + '11'
        encoded += bit_string
    return encoded

def filter_swears(text):
    with open('swears.txt', 'r') as file:
        swears = [line.strip() for line in file]
    for swear in swears:
        text = text.replace(swear, '*' * len(swear))
    return text

def send():
    message = entry.get()
    filtered_message = filter_swears(message)
    encoded_message = encode(filtered_message)
    text_output.insert(tk.END, f"Encoded message: {encoded_message}\n")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(('127.0.0.1', 12345))
        client_socket.send(encoded_message.encode())
        client_socket.close()
    except ConnectionRefusedError:
        text_output.insert(tk.END, "Failed to connect to the server.\n")

root = tk.Tk()
root.title("Client")

entry = tk.Entry(root, width=50)
entry.pack()

send_button = tk.Button(root, text="Send", command=send)
send_button.pack()

text_output = tk.Text(root, height=10, width=50)
text_output.pack()

root.mainloop()
