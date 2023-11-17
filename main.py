# coding: UTF-8
import os

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
    if not file.endswith(".encr"):
        encrypted_file = file + ".encr"  # Ajouter l'extension ".encr" au nom du fichier
        print("[!] Chiffrement du fichier : " + file)
        f = bytearray(open(file, 'rb').read())
        password = password.encode('utf-8')  # Encodage du mot de passe en UTF-8
        size = len(f)
        xord_byte_array = bytearray(size)
        for i in range(size):
            xord_byte_array[i] = f[i] ^ password[i % len(password)]  # Application cyclique du mot de passe
        open(encrypted_file, 'wb').write(xord_byte_array)
        print("[+] Fichier chiffré : " + encrypted_file)
        os.remove(file)  # Supprimer l'ancien fichier
    else:
        print("[!] Le fichier est déjà chiffré : " + file)

def decryptFile(file, password):
    if file.endswith(".encr"):
        decrypted_file = file.replace(".encr", "")  # Retirer l'extension ".encr" du nom du fichier
        print("[!] Déchiffrement du fichier : " + file)
        f = bytearray(open(file, 'rb').read())
        password = password.encode('utf-8')  # Encodage du mot de passe en UTF-8
        size = len(f)
        xord_byte_array = bytearray(size)
        for i in range(size):
            xord_byte_array[i] = f[i] ^ password[i % len(password)]  # Application cyclique du mot de passe
        open(decrypted_file, 'wb').write(xord_byte_array)
        print("[+] Fichier déchiffré : " + decrypted_file)
        os.remove(file)  # Supprimer l'ancien fichier
    else:
        print("[!] Le fichier n'est pas chiffré : " + file)

file_list = walk(path)
password = input("Entrez le mot de passe pour chiffrer/déchiffrer les fichiers : ")

for file in file_list:
    if file.endswith(".encr"):
        decryptFile(file, password)
    else:
        encryptFile(file, password)

print("[!] " + str(len(file_list)) + " fichiers traités dans le dossier " + path + ".")

