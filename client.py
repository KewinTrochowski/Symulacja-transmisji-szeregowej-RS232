import sys
import socket
import ipaddress
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QWidget, QDialog, QLineEdit
from server import CustomDialog


class ClientApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ip_address = ""
        self.port = 0
        self.set_ip_and_port()
        self.initUI()
        while True:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                client_socket.connect((self.ip_address, self.port))
                client_socket.close()
                break
            except ConnectionRefusedError:
                print("Failed to connect to the server.")
                self.set_ip_and_port()

    def initUI(self):
        self.setWindowTitle('Client')
        self.setGeometry(100, 100, 500, 300)

        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)

        self.lineEdit = QLineEdit()

        self.sendButton = QPushButton("Send")
        self.sendButton.clicked.connect(lambda: self.send())

        layout = QVBoxLayout()
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.sendButton)
        layout.addWidget(self.textEdit)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def encode(self, text):
        encoded = ""
        for char in text:
            ascii_value = ord(char)
            bit_string = '0' + format(ascii_value, '08b')[::-1] + '11'
            encoded += bit_string
        return encoded

    def filter_swears(self, text):
        swears = [l for l in open('swears.txt').read().split('\n') if l != '']
        for swear in swears:
            text = text.replace(swear, '*' * len(swear))
        return text

    def send(self):
        message = self.lineEdit.text()
        filtered_message = self.filter_swears(message)
        encoded_message = self.encode(filtered_message)
        self.textEdit.append(f"Encoded message: {encoded_message}\n")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((self.ip_address, self.port))
            client_socket.send(encoded_message.encode())
            client_socket.close()
        except ConnectionRefusedError:
            self.textEdit.append("Failed to connect to the server.\n")


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



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ClientApp()
    ex.show()
    sys.exit(app.exec())
