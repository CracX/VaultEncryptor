from cryptography.fernet import Fernet
from base64 import b64encode
import argparse
from getpass import getpass
import sys
import os

argpar = argparse.ArgumentParser(description='An encryptor that encrypts/decrypts files in the vault directory.')
argpar.add_argument('-i', help="Interactive mode", action='store_const', const=True)
argpar.add_argument('-e', help="Encrypt", action='store_const', const=True)
argpar.add_argument('-d', help="Decrypt", action='store_const', const=True)

'''
k1 = input("Enter key: ")
k2 = b64encode((k1 + ("="*(32-len(k1)))).encode())

f = Fernet(k2)
'''

def encrypt(key, content):
    f = Fernet(key)
    print(key)
    return f.encrypt(content)

def decrypt(key, content):
    f = Fernet(key)
    print(key)
    return f.decrypt(content)

if __name__ == "__main__":
    ROOT_PATH = "vault"

    if not os.path.isdir(ROOT_PATH):
        os.mkdir(ROOT_PATH)

    args = argpar.parse_args()
    if args.e and args.i:
        print("Conflicting arguments: -e and -d cant be used together.")
        sys.exit(1)
    
    if not args.i:
        if args.e:
            k = getpass("Enter key: ")
            if len(k) > 32:
                print("Key cannot be bigger than 32 characters.")
                sys.exit(1)
            k = b64encode((k + ("="*(32-len(k)))).encode())
            files_list = os.listdir(ROOT_PATH)
            for file in files_list:
                with open(f"{ROOT_PATH}/{file}", "w+") as f:
                    old_content = f.read().encode()
                    f.write(encrypt(k, old_content).decode())
                os.rename(f"{ROOT_PATH}/{file}", f"{ROOT_PATH}/{file}.enc")
                print(f"Encrypted {file}...")
            print("Done")
            sys.exit(0)
        
        if args.d:
            k = getpass("Enter key: ")
            if len(k) > 32:
                print("Key cannot be bigger than 32 characters.")
                sys.exit(1)
            k = b64encode((k + ("="*(32-len(k)))).encode())
            
            files_list = os.listdir(ROOT_PATH)
            for file in files_list:
                with open(f"{ROOT_PATH}/{file}", "w+") as f:
                    old_content = f.read().encode()
                    print(old_content)
                    f.write(decrypt(k, old_content).decode())
                os.rename(f"{ROOT_PATH}/{file}", f"{ROOT_PATH}/{file[0:-4]}")
                print(f"Decrypted {file[0:-4]}...")
            print("Done")
            sys.exit(0)
