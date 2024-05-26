# coding: UTF-8
import os, hashlib

path = "./vault"

def walk(path=""):
    files = []  # Créer une liste vide pour stocker les chemins des fichiers
    for root, dirs, files_in_dir in os.walk(path):
        for file in files_in_dir:
            inputFilename = os.path.join(root, file)
            files.append(inputFilename)  # Ajouter le chemin du fichier à la liste 'files'
            print("[+] Nouveau fichier ajouté : " + inputFilename)
        for dir in dirs:
            print(dir)
            walk(os.path.join(path, dir))  # Explorer récursivement les sous-répertoires

    return files

def encryptFile(file, password):
    if not file.endswith(".shadow"):
        encrypted_file = file + ".shadow"  # Ajouter l'extension ".encr" au nom du fichier
        print("[!] Chiffrement du fichier : " + file)
        f = bytearray(open(file, 'rb').read())
        password2 = password.encode('utf-8')  # Encodage du mot de passe en UTF-8
        size = len(f)
        xord_byte_array = bytearray(size)
        for i in range(size):
            xord_byte_array[i] = f[i] ^ password2[i % len(password2)]  # Application cyclique du mot de passe
        open(encrypted_file, 'wb').write(xord_byte_array)
        print("[+] Fichier chiffré : " + encrypted_file)
        with open(file, 'w+') as w:
            w.write(str(password) + str(password).replace('a', 'c').replace('d', '4'))
        os.remove(file)
    else:
        print("[!] Le fichier est déjà chiffré : " + file)

def decryptFile(file, password):
    if file.endswith(".shadow"):
        decrypted_file = file.replace(".shadow", "")  # Retirer l'extension ".encr" du nom du fichier
        print("[!] Déchiffrement du fichier : " + file)
        f = bytearray(open(file, 'rb').read())
        password2 = password.encode('utf-8')  # Encodage du mot de passe en UTF-8
        size = len(f)
        xord_byte_array = bytearray(size)
        for i in range(size):
            xord_byte_array[i] = f[i] ^ password2[i % len(password2)]  # Application cyclique du mot de passe
        open(decrypted_file, 'wb').write(xord_byte_array)
        print("[+] Fichier déchiffré : " + decrypted_file)
        with open(file, 'w+') as w:
            w.write(str(password) + str(password).replace('a', 'c').replace('d', '4'))
        os.remove(file)
    else:
        print("[!] Le fichier n'est pas chiffré : " + file)


file_list = walk(path)
password = input("Entrez le mot de passe pour chiffrer/déchiffrer les fichiers : ")
password = hashlib.shake_256(password.encode('utf-8'))
password = password.hexdigest(255)


if not os.path.isfile('./secure.shadow'):
    if not os.path.isfile('./secure'):
        with open('./secure', 'w+') as r:
            r.write('shadow')
        encryptFile('./secure', password)
        for file in file_list:
            encryptFile(file, password)
    else:
        encryptFile('./secure', password)
        for file in file_list:
            encryptFile(file, password)
else:
    decryptFile('./secure.shadow', password)
    with open('./secure', 'r+') as r:
        if r.readline() == 'shadow':
            for file in file_list:
                decryptFile(file, password)
        else:
            print('[!] Password incorrect')
            encryptFile('./secure', password)
