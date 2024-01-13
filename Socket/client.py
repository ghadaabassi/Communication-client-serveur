from tkinter import *
from flask import Flask, request, jsonify
import threading
import socket
from server import run_socket_server

import tkinter as tk
from PIL import Image, ImageTk

app = Flask(__name__)

@app.route("/", methods=["POST"])
def handle_request():
    try:
        data = request.get_json()
        if "method" in data and "params" in data:
            method = data["method"]
            params = data["params"]
            result = process_request(method, params)
            response = {"status": "success", "result": result, "id": data.get("id")}
        else:
            response = {"status": "error", "message": "Invalid Request", "id": data.get("id")}
    except Exception as e:
        response = {"status": "error", "message": "Internal error", "data": str(e), "id": data.get("id")}

    return jsonify(response)

def process_request(method, params):
    if method == "ConvertDollar":
        return params.get("a", 0) * 3
    if method == "ConvertEuro":
        return params.get("a", 0) * 3.5

class SocketClient:
    def __init__(self):
        self.server_address = ("localhost", 5556)

    def send_request(self, method, params):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(self.server_address)
            data = f"{method};{params}"
            s.sendall(data.encode())
            result = s.recv(1024).decode()
            return result

class SocketClientGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Conversion",)
        self.root.configure(bg="white")
        
        image = Image.open('mn.jpg')

        resized_image = image.resize((270, 270))

        tk_image = ImageTk.PhotoImage(resized_image)
        self.logo_image = tk_image
        
        self.logo_label = tk.Label(self.root, image=self.logo_image )
        self.logo_label.pack(side="left")

        frame = tk.Frame(self.root , background="white")
        
        frame.pack(side="left", padx=10)

        self.message_display = tk.Text(frame, height=15, width=70, font=("Arial", 16))
        self.message_display.pack()

        self.request_button = tk.Button(frame, text="Convert", command=self.make_requests, font=("Arial", 18) , background="#fffff0")
        self.request_button.pack(side="bottom", pady=10)

    def make_requests(self):
       
        self.message_display.delete(1.0, END)
        self.display_message("\t\t\t Conversion du DT\n")

        client = SocketClient()
        result_dollar = client.send_request("ConvertDollar", 15)
        result_euro = client.send_request("ConvertEuro", 15)

        self.display_message(f"Resultat de ConvertDollar: 15DT --> {result_dollar} $\n")
        self.display_message(f"Resultat de ConvertEuro: 15DT --> {result_euro} €\n")

    def display_message(self, message):
    
        self.message_display.insert(END, f"{message}\n")
        self.message_display.see(END)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    threading.Thread(target=run_socket_server, daemon=True).start()
    SocketClientGUI().run()
