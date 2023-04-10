from tkinter import *
from tkinter import messagebox, Checkbutton, IntVar, StringVar
import tkinter.filedialog as filedialog
import os

from rsa import *
from main import StartPage

class SignageUI(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Functions & Variables

        isStoredSeparately = IntVar(value = 0)
        msgFilePath = StringVar(value = '')
        msgFileName = StringVar(value = '')
        message = StringVar(value = '')
        
        projectTitle = Label(
            self,
            text="Generate Signature"
        )
        projectTitle.pack()

        loadMessageButton = Button(
            self,
            text="Load",
            padx= 10,
            pady= 10,
            bg="blue",
            fg="yellow",
            command = self.loadMessage
        )
        loadMessageButton.pack()

        signatureStorage = Checkbutton(self,text='Store signature separately',variable=isStoredSeparately, onvalue=1, offvalue=0)
        signatureStorage.pack()

        signFileButton = Button(
            self,
            text="Sign file",
            padx= 10,
            pady= 10,
            bg="#6b5b95",
            fg="#feb236",
            command = self.signFile
        )
        signFileButton.pack()

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
        fileNameLabel = Label(
            self,
            text=fileName
        )
        fileNameLabel.pack()

        self.message.set(open(textfile).read())

    def signFile(self):
        try:
            file = open('key.pri', 'r')
            privKey = file.read()

        except:
            messagebox.showinfo(self,title="Error!", message="Private key not detected.")

        hashDigest = int(hashText(self.message.get()))
        # TODO: figure out what to do with n
        signature = encryptSignature(hashDigest, privKey, n = 23*7)

        if self.isStoredSeparately.get():
            saveSignatureSeparated(signature)
            messagebox.showinfo(self,title="Success!", message="Signature successfully stored separately in file signature.txt.")
        else:
            insertSignature(self.msgFilePath.get(), signature)
            messagebox.showinfo(self,title="Success!", message="Signature successfully stored in file " + self.msgFileName.get() + ".")