from tkinter import *
from tkinter import messagebox, Checkbutton, IntVar, StringVar
import os
import tkinter.filedialog as filedialog

from rsa import *

class Main(Tk):
    def __init__(self, *args, **kwargs):
        
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)
        
        container.pack()

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        

        self.frames = {}

        for F in (StartPage, KeysUI, SignageUI, VerificationUI):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)


    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

class StartPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        projectTitle = Label(
            self,
            text="Digital Signage"
        )
        projectTitle.pack()
        
        generateKeyButton = Button(
            self,
            text="Generate Keys",
            padx= 10,
            pady= 10,
            bg="#19323c",
            fg="#f3f7f0",
            command = lambda: controller.show_frame(KeysUI)  
        )
        generateKeyButton.pack()

        generateSignatureButton = Button(
            self,
            text="Generate Signature",
            padx= 10,
            pady= 10,
            bg="#19323c",
            fg="#f3f7f0",
            command = lambda: controller.show_frame(SignageUI)
        )
        generateSignatureButton.pack()

        verifySignatureButton = Button(
            self,
            text="Verify Signature",
            padx= 10,
            pady= 10,
            bg="#19323c",
            fg="#f3f7f0",
            command = lambda: controller.show_frame(VerificationUI)
        )
        verifySignatureButton.pack()

class KeysUI(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        
        projectTitle = Label(
            self,
            text="Generate Keys",
            fg="#000807"
        )
        projectTitle.pack()

        pLabel = Label(
            self,
            text="p"
        )
        pLabel.pack()

        self.pTextbox = Entry(self)
        self.pTextbox.pack()

        qLabel = Label(
            self,
            text="q"
        )
        qLabel.pack()

        self.qTextbox = Entry(self)
        self.qTextbox.pack()

        generateKeyButton = Button(
            self,
            text="Generate Keys",
            padx= 10,
            pady= 10,
            bg="#19323c",
            fg="#f3f7f0",
            command = self.generateKeys
        )
        generateKeyButton.pack()

        backButton = Button(
            self,
            text="Back",
            padx= 10,
            pady= 10,
            bg="#8c5e58",
            fg="#f3f7f0",
            command = lambda: controller.show_frame(StartPage)
        )
        backButton.pack()

    def generateKeys(self):
        p = self.pTextbox.get()
        q = self.qTextbox.get()

        if not p or not q:
            messagebox.showinfo(title="Error!", message="Please enter both your p and q values.")
        else:
            if not prime(int(p)):
                messagebox.showinfo(title="Attention!", message="P value is not prime. Please re-enter its value.")
            elif not prime(int(q)):
                messagebox.showinfo(title="Attention!", message="Q value is not prime. Please re-enter its value.")
            else:
                pubKey, privKey = getKey(int(p), int(q))

                saveGeneratedKeys(pubKey, privKey)

                messagebox.showinfo(title="Success!", message="Public and private keys successfully generated.")

class VerificationUI(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Functions & Variables

        self.isStoredSeparately = IntVar(value = 0)
        self.msgFilePath = StringVar(value = '')
        self.msgFileName = StringVar(value = '')
        self.signatureVar = StringVar(value = '')
        self.messageVar = StringVar(value = '')

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
            bg="#a93f55",
            fg="#f3f7f0",
            command = self.loadMessage
        )
        loadMessageButton.pack()

        pLabel = Label(
            self,
            text="p"
        )
        pLabel.pack()

        self.pTextbox = Entry(self)
        self.pTextbox.pack()

        qLabel = Label(
            self,
            text="q"
        )
        qLabel.pack()

        self.qTextbox = Entry(self)
        self.qTextbox.pack()

        signatureStorage = Checkbutton(self,text='Separate signature',variable=self.isStoredSeparately, onvalue=1, offvalue=0)
        signatureStorage.pack()

        verifySignatureButton = Button(
            self,
            text="Verify Signature",
            padx= 10,
            pady= 10,
            bg="#19323c",
            fg="#f3f7f0",
            command = self.verifySignature
        )
        verifySignatureButton.pack()

        backButton = Button(
            self,
            text="Back",
            padx= 10,
            pady= 10,
            bg="#8c5e58",
            fg="#f3f7f0",
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
            messagebox.showinfo(title="Error!", message="Signature not detected. Did you store the signature separately?")
        else:
            fileNameLabel = Label(
                self,
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
            messagebox.showinfo(title="Error!", message="Public key not detected.")

        p = self.pTextbox.get()
        q = self.qTextbox.get()

        if not p or not q:
            messagebox.showinfo(title="Error!", message="Please enter both your p and q values.")
        
        else:
            hashDigest = int(hashText(self.messageVar.get()))

            signature = self.signatureVar.get()

            if not (self.isStoredSeparately.get()):
                signature = getSignature(self.msgFilePath.get())

            decryptedSignature = decryptSignature(signature, pubKey, int(p)*int(q))

            isSignatureAuthentic = authenticateSignature(hashDigest, decryptedSignature, int(p)*int(q))
            if isSignatureAuthentic:
                messagebox.showinfo(title="Success!", message="Signature is verified as authentic.")
            else:
                messagebox.showinfo(title="Error!", message="Signature is not authentic!")

class SignageUI(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Functions & Variables

        self.isStoredSeparately = IntVar(value = 0)
        self.msgFilePath = StringVar(value = '')
        self.msgFileName = StringVar(value = '')
        self.message = StringVar(value = '')
        
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
            bg="#a93f55",
            fg="#f3f7f0",
            command = self.loadMessage
        )
        loadMessageButton.pack()

        pLabel = Label(
            self,
            text="p"
        )
        pLabel.pack()

        self.pTextbox = Entry(self)
        self.pTextbox.pack()

        qLabel = Label(
            self,
            text="q"
        )
        qLabel.pack()

        self.qTextbox = Entry(self)
        self.qTextbox.pack()

        signatureStorage = Checkbutton(self,text='Store signature separately',variable=self.isStoredSeparately, onvalue=1, offvalue=0)
        signatureStorage.pack()

        signFileButton = Button(
            self,
            text="Sign file",
            padx= 10,
            pady= 10,
            bg="#19323c",
            fg="#f3f7f0",
            command = self.signFile
        )
        signFileButton.pack()

        backButton = Button(
            self,
            text="Back",
            padx= 10,
            pady= 10,
            bg="#8c5e58",
            fg="#f3f7f0",
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
            messagebox.showinfo(title="Error!", message="Private key not detected.")

        p = self.pTextbox.get()
        q = self.qTextbox.get()

        if not p or not q:
            messagebox.showinfo(title="Error!", message="Please enter both your p and q values.")

        else:
            hashDigest = int(hashText(self.message.get()))
            signature = encryptSignature(hashDigest, int(privKey), int(p)*int(q))

            if self.isStoredSeparately.get():
                saveSignatureSeparated(signature)
                messagebox.showinfo(title="Success!", message="Signature successfully stored separately in file signature.txt.")
            else:
                insertSignature(self.msgFilePath.get(), signature)
                messagebox.showinfo(title="Success!", message="Signature successfully stored in file " + self.msgFileName.get() + ".")

# Start the app
root = Main()
root.title("Kriptografi, Tucil 3")
root.geometry("500x400")
root.mainloop()