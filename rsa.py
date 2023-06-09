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
    c = 0
    while(c != 1):
        pubKey = random.randrange(1, a)
        c = fpb(pubKey, a)
    return pubKey
  
def createPrivKey(totient, e):
    k = 1
    d = (1+(k*totient))/e   
    while(d != int(d)):
        k += 1
        d = (1+(k*totient))/e
    return int(d)     

def getKey(p, q):
    if(prime(p) and prime(q)):
        n = p*q
        totient = (p-1)*(q-1)
        pubKey = createPubKey(totient)
        privKey = createPrivKey(totient, pubKey)
        return pubKey, privKey
        
# Verifying Signature
def getMessage(filename):
    file = open(filename, 'r')
    msg = file.read()
    
    # Find where the <ds> </ds> is located
    openingTag = msg.find('<ds>')
    closingTag = msg.find('</ds>')

    if not ((openingTag == -1) or (closingTag == -1)):
        return(msg[:openingTag])
    else: 
       return msg
    
def getSignature(filename):
    file = open(filename, 'r')
    msg = file.read()
    
    # Find where the <ds> </ds> is located
    openingTag = msg.find('<ds>')
    closingTag = msg.find('</ds>')

    if not ((openingTag == -1) or (closingTag == -1)):
        signature = msg[openingTag+4:closingTag]
        return signature
    else: 
       return False
    
def getSignatureAndMessage(filename):
    file = open(filename, 'r')
    msg = file.read()
    
    # Find where the <ds> </ds> is located
    openingTag = msg.find('<ds>')
    closingTag = msg.find('</ds>')


    if not ((openingTag == -1) or (closingTag == -1)):
        signature = msg[openingTag+4:closingTag]
        msgOnly = msg[:openingTag]
        return (signature, msgOnly)
    else: 
       return (False, False)

# Hash text
def hashText(text):
    msgDigest  = hashlib.sha3_256(text.encode('UTF-8'))
    msgHex = msgDigest.hexdigest()
    msgDec = int(msgHex,16)
    return msgDec

def encryptSignature(hashDigest, privKey, n):
    return (int(hashDigest)**int(privKey)) % n

def decryptSignature(signature, publicKey, n):
    return (int(signature)**int(publicKey)) % n

def authenticateSignature(hashDigest, decryptSignature, n):
    return decryptSignature == (hashDigest%n)

def insertSignature(filename, signature):
    file = open(filename, 'r')
    msg = file.read()
    
    newFile = open(filename, 'w')
    signTags = '<ds>' + str(signature) + '</ds>'
    newFile.write(msg + signTags)

def saveSignatureSeparated(signature):
    newFile = open('signature.txt', 'w')
    signTags = '<ds>' + str(signature) + '</ds>'
    newFile.write(signTags)

def saveGeneratedKeys(pubKey, privKey):
    privFile = open('key.pri', 'w')
    privFile.write(str(privKey))

    pubFile = open('key.pub', 'w')
    pubFile.write(str(pubKey))