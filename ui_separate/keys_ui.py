from tkinter import *
from tkinter import messagebox
import tkinter.filedialog as filedialog

from rsa import *
from main import StartPage

class KeysUI(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        
        projectTitle = Label(
            self,
            text="Generate Keys"
        )
        projectTitle.pack()

        pLabel = Label(
            self,
            text="p"
        )
        pLabel.pack()

        pTextbox = Entry(self)
        pTextbox.pack()

        qLabel = Label(
            self,
            text="q"
        )
        qLabel.pack()

        qTextbox = Entry(self)
        qTextbox.pack()

        generateKeyButton = Button(
            self,
            text="Generate Keys",
            padx= 10,
            pady= 10,
            bg="#6b5b95",
            fg="#feb236",
            command = self.generateKeys
        )
        generateKeyButton.pack()

        backButton = Button(
            self,
            text="Back",
            padx= 10,
            pady= 10,
            bg="#6b5b95",
            fg="#feb236",
            command = lambda: controller.show_frame(StartPage)
        )
        backButton.pack()

    def generateKeys(self):
        p = self.pTextbox.get()
        q = self.qTextbox.get()

        if not p or not q:
            messagebox.showinfo(self,title="Error!", message="Please enter both your p and q values.")
        else:
            if not prime(int(p)):
                messagebox.showinfo(self,title="Attention!", message="P value is not prime. Please re-enter its value.")
            elif not prime(int(q)):
                messagebox.showinfo(self,title="Attention!", message="Q value is not prime. Please re-enter its value.")
            else:
                pubKey, privKey = getKey(int(p), int(q))

                saveGeneratedKeys(pubKey, privKey)

                messagebox.showinfo(self,title="Success!", message="Public and private keys successfully generated.")