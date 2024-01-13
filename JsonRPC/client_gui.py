import tkinter as tk

import requests
import json
from PIL import Image, ImageTk


class JsonRpcClient:
    def __init__(self, url):
        self.url = url

    def make_request(self, method, params):
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": 1
        }

        headers = {'Content-Type': 'application/json'}
        response = requests.post(self.url, data=json.dumps(payload), headers=headers)

        try:
            response.raise_for_status()
            result = response.json().get("result")

            if result is not None:
                result_message = f"   Resultat de {method}: 15 DT -->  {result} \n"
                client_gui.display_message(result_message)
            else:
                error_message = f"Error: {response.json().get('error')}"
                client_gui.display_message(error_message)
        except requests.exceptions.HTTPError as e:
            error_message = f"HTTP Error: {e}"
            client_gui.display_message(error_message)
        except json.JSONDecodeError as e:
            error_message = f"JSON Decode Error: {e}"
            client_gui.display_message(error_message)

class JsonRpcClientGUI:
    def __init__(self, url):
        self.url = url

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
        self.message_display.delete(1.0, tk.END)
        self.display_message("\t\t\t Conversion du DT\n")

        client = JsonRpcClient(self.url)
        client.make_request("ConvertDollar", {"a": 15})
        client.make_request("ConvertEuro", {"a": 15})

    def display_message(self, message):
        self.message_display.insert(tk.END, f"{message}\n")
        self.message_display.see(tk.END)


    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    client_gui = JsonRpcClientGUI("http://localhost:5000")
    client_gui.run()
