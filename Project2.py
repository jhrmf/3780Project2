#By Jackson Hoenig and Joe Hill
import base64
import os
import string
import random
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import hashlib, binascii
from itertools import product
import time
numOfHashes = 1;
def hash_password_plain(password):
    salt = hashlib.sha256(b"1").hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, numOfHashes)
    pwdhash = binascii.hexlify(pwdhash)
    return (pwdhash).decode('ascii')

def verify_password_plain(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    #no salt
    salt = hashlib.sha256(b"1").hexdigest().encode('ascii')
    #stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt,
                                  numOfHashes)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

def hash_password_salt(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, numOfHashes)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password_salt(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  numOfHashes)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

#task 1 is a function that can be called multiple times
#it will print to all 3 file types
def task2(passBound,numOfAcc):
    out1 = open("db1.txt", "w+")
    out2 = open("db2.txt", "w+")
    out3 = open("db3.txt", "w+")
    for x in range(numOfAcc):
        #print uname
        out1.write("user" + str(x) + ", ")
        out2.write("user" + str(x) + ", ")
        out3.write("user" + str(x) + ", ")
        password = "";
        #generate password
        for i in range(passBound):
            password += random.choice(string.ascii_lowercase)

        #print(password)

        plain_hash = hash_password_plain(password)
        salt_hash = hash_password_salt(password)

        #generate password
        out1.write(password + "\n")
        out2.write(plain_hash + "\n")
        out3.write(salt_hash + "\n")
        #out2.write(str(token2) + ", " + str.decode(key2) + "\n")
        #out3.write(str(token3) + ", " + str(key3) + ", " + str(salt) + "\n")

def verify(password,uname):
    inf1 = open("db1.txt", "r")
    inf2 = open("db2.txt", "r")
    inf3 = open("db3.txt", "r")

#verify first file
    for line in inf1:

        list = line.split(", ")
        if str(list[0]) == str(uname):
            if list[1].rstrip() == password.rstrip():
                print("Matched first file")
            else:
                print("Invalid Login on first file")
            break;

#verify second file
#uname, hashedToken, key
    for line in inf2:

        list = line.split(", ")
        if str(list[0]) == str(uname):
            if verify_password_plain(list[1].rstrip(),password):
                print("Matched second file")
            else:
                print("Invalid Login on second file")
            break;
#verify third file
#uname, hashedToken, key, salt
    for line in inf3:

        list = line.split(", ")
        if str(list[0]) == str(uname):
            if verify_password_salt(list[1].rstrip(),password):
                print("Matched third file")
            else:
                print("Invalid Login on third file")
            break;


def crackPassword(fileNumber,passwordSize):
    if(fileNumber == 2):
        infile = open("db2.txt", "r")
        # flag = False
        # while(flag):
        for i in range(passwordSize + 1):
            for attempt in product('abcdefghijklmnopqrstuvwxyz', repeat=i):
                #print(''.join(attempt))
                for line in infile:
                    list = line.split(", ")
                    if verify_password_plain(list[1].rstrip(), ''.join(attempt)):
                        print("Cracked file of type 2: username: " + str(list[0]) + " password: " + ''.join(attempt))
                        return True
                infile.seek(0)


    else:
        infile = open("db3.txt", "r")
        line = infile.readline()
        list = line.split(", ")
        flag = False
        #generator=itertools.combinations_with_replacement('abcdefghijklmnopqrstuvwxyz', passwordSize)
        for i in range(passwordSize + 1):
            for attempt in product('abcdefghijklmnopqrstuvwxyz', repeat=i):
                #print(''.join(attempt))
                if verify_password_salt(list[1].rstrip(),''.join(attempt)):
                    print("Cracked file of type 3: username: " + str(list[0]) + " password: " + ''.join(attempt))
                    return True

#driver:

numOfHashes = 1;
passwordLength = 5;


print("Starting program...")


#verify(password,uname)


for x in range(10):
    file = open("output.txt", "a")
    passwordLength = x
    task2(passwordLength, 10);
    start_time = time.time()
    crackPassword(2,passwordLength)
    print("Time To Crack file 2 for " + str(x) + ": " + str( time.time() - start_time))
    file.write("Time To Crack file 2 for " + str(x) + ": " + str( time.time() - start_time) + "\n")

    start_time = time.time()
    crackPassword(3,passwordLength)
    print("Time To Crack file 3 for " + str(x) + ": " + str( time.time() - start_time))
    file.write("Time To Crack file 3 for " + str(x) + ": " + str( time.time() - start_time) + "\n")
    file.close()


#input = input("type 'stop' and press enter to end otherwise just press enter to try again")

