from tkinter import *
from tkinter import messagebox, Checkbutton, IntVar, StringVar
import tkinter.filedialog as filedialog
import os

from rsa import *
from main import StartPage


class VerificationUI(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Functions & Variables

        isStoredSeparately = IntVar(value = 0)
        msgFilePath = StringVar(value = '')
        msgFileName = StringVar(value = '')
        signatureVar = StringVar(value = '')
        messageVar = StringVar(value = '')

        projectTitle = Label(
            self,
            text="Verify Signature"
        )
        projectTitle.pack()


        loadMessageButton = Button(
            self,
            text="Load Text",
            padx= 10,
            pady= 10,
            bg="blue",
            fg="yellow",
            command = self.loadMessage
        )
        loadMessageButton.pack()

        fileNameLabel = Label(
            self,
            text=msgFileName.get()
        )
        fileNameLabel.pack()

        signatureStorage = Checkbutton(self,text='Separate signature',variable=isStoredSeparately, onvalue=1, offvalue=0)
        signatureStorage.pack()

        verifySignatureButton = Button(
            self,
            text="Verify Signature",
            padx= 10,
            pady= 10,
            bg="#6b5b95",
            fg="#feb236",
            command = self.verifySignature
        )
        verifySignatureButton.pack()

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

    # Load text
    def loadMessage(self):
        textfile = filedialog.askopenfilename(initialdir = ".",
                title = "Select a File",
                filetypes = (("Text files",
                            "*.txt*"),
                            ("all files",
                            "*.*")))
        fileName = os.path.split(textfile)[1]
        self.msgFilePath.set(textfile)
        self.msgFileName.set(fileName)

        if (self.isStoredSeparately.get()):
            message = getMessage(textfile)
            signature = getSignature(os.getcwd()+"\\signature.txt")

        else:
            signature, message = getSignatureAndMessage(textfile)

        if not signature:
            messagebox.showinfo(self,title="Error!", message="Signature not detected. Did you store the signature separately?")
        else:
            fileNameLabel = Label(
                text=fileName
            )
            fileNameLabel.pack()
            self.signatureVar.set(int(signature))
            self.messageVar.set(message)

    def verifySignature(self):
        try:
            file = open('key.pub', 'r')
            pubKey = file.read()

        except:
            messagebox.showinfo(self,title="Error!", message="Public key not detected.")

        hashDigest = int(hashText(self.messageVar.get()))
        # TODO: figure out what to do with n
        decryptedSignature = decryptSignature(self.signatureVar.get(), pubKey, n = 23*7)

        isSignatureAuthentic = authenticateSignature(hashDigest, decryptedSignature, n = 23*7)
        print(isSignatureAuthentic)
        if isSignatureAuthentic:
            messagebox.showinfo(self,title="Success!", message="Signature is verified as authentic.")
        else:
            messagebox.showinfo(self,title="Error!", message="Signature is not authentic!")