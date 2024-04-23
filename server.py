import sys
import socket
import threading
import ipaddress
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QInputDialog, QDialog, QLabel, QLineEdit, QPushButton

class ServerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.ip_address = ""
        self.port = 0
        self.set_ip_and_port()

        self.thread = threading.Thread(target=self.start_server)
        self.thread.start()

    def initUI(self):
        self.setWindowTitle('Server')
        self.setGeometry(100, 100, 500, 400)

        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.textEdit)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def decode(self, bit_string):
        chars = []
        for i in range(0, len(bit_string), 11):
            byte = bit_string[i+1:i+9]
            ascii_value = int(byte[::-1], 2)
            chars.append(chr(ascii_value))
        return ''.join(chars)

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                self.server_socket.bind((self.ip_address, self.port))
                break
            except OSError as e:
                print(f"Failed to bind: {e}")
                self.set_ip_and_port()
        self.server_socket.listen(1)
        while True:
            client_socket, addr = self.server_socket.accept()
            thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            thread.start()

    def handle_client(self, client_socket):
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            decoded_message = self.decode(data)
            self.textEdit.append(f"Received: {decoded_message}\n")
        client_socket.close()

    def set_ip_and_port(self):
        dialog = CustomDialog(self)
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            ip, port_str = dialog.get_data()
            try:
                if self.validate_ip(ip) and 1 <= int(port_str) <= 65535:
                    self.ip_address = ip
                    self.port = int(port_str)
                    print(f"IP: {self.ip_address}, Port: {self.port}")
                else:
                    raise ValueError("Invalid IP or port.")
            except ValueError as ve:
                print(f"Error: {ve}")
                self.set_ip_and_port()
        else:
            print("Input cancelled.")

    def validate_ip(self, ip):
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False

class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Enter IP and Port")
        layout = QVBoxLayout()

        self.ip_label = QLabel("IP Address:", self)
        self.ip_input = QLineEdit(self)
        layout.addWidget(self.ip_label)
        layout.addWidget(self.ip_input)
        self.ip_input.setText("127.0.0.1")

        self.port_label = QLabel("Port (1-65535):", self)
        self.port_input = QLineEdit(self)
        layout.addWidget(self.port_label)
        layout.addWidget(self.port_input)
        self.port_input.setText("12345")

        self.button_ok = QPushButton("OK", self)
        self.button_ok.clicked.connect(self.accept)
        self.button_cancel = QPushButton("Cancel", self)
        self.button_cancel.clicked.connect(self.reject)
        layout.addWidget(self.button_ok)
        layout.addWidget(self.button_cancel)

        self.setLayout(layout)

    def get_data(self):
        return self.ip_input.text(), self.port_input.text()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ServerApp()
    ex.show()
    sys.exit(app.exec())
