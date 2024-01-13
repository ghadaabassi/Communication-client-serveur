import tkinter as tk
from tkinter import PhotoImage
from xmlrpc.client import ServerProxy
import threading

from tkinter import PhotoImage
from PIL import Image, ImageTk

class XmlRpcClientGUI:
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

        self.request_button.config(state=tk.DISABLED)
        threading.Thread(target=self.perform_requests).start()

    def perform_requests(self):
        try:
            self.message_display.delete(1.0, tk.END)
            self.display_message("\t\t\t Conversion du DT\n")

            client = ServerProxy(self.url)
            result_dollar = client.ConvertDollar(15)
            result_euro = client.ConvertEuro(15)

            self.display_message(f"Resultat de ConvertDollar: 15DT --> {result_dollar} $\n")
            self.display_message(f"Resultat de ConvertEuro: 15DT --> {result_euro} €\n")
        except Exception as e:
            self.display_message(f"Error: {e}\n")
        finally:
            self.request_button.config(state=tk.NORMAL)

    def display_message(self, message):
        self.message_display.insert(tk.END, f"{message}\n")
        self.message_display.see(tk.END)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    client_gui = XmlRpcClientGUI("http://localhost:5001/xmlrpc")
    client_gui.run()

