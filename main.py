import hashlib
import random

# RSA Algorithm
def prime(a):
    prime = True
    if(a > 1):
        for i in range(2, a):
            if a % i == 0:
                prime = False
    else:
        return False
    return prime

def fpb(a, b):
    for i in range (1, min(a,b) + 1):
        if((a % i == 0) and (b % i == 0)):
            fpb = i
    return fpb

def createPubKey(a):
    e = 0
    while(e != 1):
        e = fpb(random.randrange(1, a), a)
    return e
  
def createPrivKey(n, e):
    while(d)
    d = (1+(1*))    
def encryptKey(p, q):
    if(prime(p) and prime(q)):
        n = p*q
        totient = (p-1)*(q-1)
        pubKey = createPubKey(totient)
        


def getMessage(filename):
    file = open(filename, 'r')
    msg = file.read()
    
    # Find where the <ds> </ds> is located
    openingTag = msg.find('<ds>')
    closingTag = msg.find('</ds>')

    if not ((openingTag == -1) or (closingTag == -1)):
        return(msg[:openingTag])
    else: 
       return 'File not found'
    
def getSignature(filename):
    file = open(filename, 'r')
    msg = file.read()
    
    # Find where the <ds> </ds> is located
    openingTag = msg.find('<ds>')
    closingTag = msg.find('</ds>')

    if not ((openingTag == -1) or (closingTag == -1)):
        return(msg[openingTag+4:closingTag])
    else: 
       return 'File not found'

# Hash text
def hashText(text):
    msgDigest  = hashlib.sha3_512(text.encode('UTF-8'))
    msgHex = msgDigest.hexdigest()
    msgDec = int(msgHex,16)
    return msgDec

def encryptSignature(hashDigest, privKey, n):
    return (hashDigest**privKey) % n

def decryptSignature(signature, publicKey, n):
    return (signature**publicKey) % n

def isSignatureAuthentic(hashDigest, hashDecrypt):
    return hashDigest == hashDecrypt

def insertSignature(filename, signature):
    file = open(filename, 'r')
    msg = file.read()
    
    newFile = open(filename, 'w')
    signTags = '<ds>' + str(signature) + '</ds>'
    newFile.write(msg + signTags)

def saveSignatureSeparated(signature):
    newFile = open('signature', 'w')
    signTags = '<ds>' + str(signature) + '</ds>'
    newFile.write(signTags)

print(hashText('asdf'))
