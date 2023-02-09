# Ce code est une implémentation simple d'un service RSA basé sur Flask.
# Il génère une paire de clés RSA publique et privée de 2048 bits.
# Il fournit une API avec deux points de terminaison:
# 1. /rsa/public_key/ pour renvoyer la clé publique.
# 2. /rsa/logs/ pour recevoir et déchiffrer les messages postés avec la clé privée.

import base64
from flask import Flask, request
import rsa

app = Flask(__name__)

# Génération des clés RSA
public_key, private_key = rsa.newkeys(2048)

# Affichage de la clé publique et privée
print(public_key.save_pkcs1().decode())
print(private_key.save_pkcs1().decode())

# Stockage des messages déchiffrés
deciphered_message = ''


# Point de terminaison pour renvoyer la clé publique
@app.route('/rsa/public_key/', methods=['GET'])
def public_key_endpoint():
    return public_key.save_pkcs1().decode()


# Point de terminaison pour déchiffrer et stocker les messages
@app.route('/rsa/logs/', methods=['GET', 'POST'])
def logs_endpoint():
    global deciphered_message
    if request.method == 'POST':
        # Déchiffrement du message posté avec la clé privée
        deciphered_message = base64.b64decode(request.form["message"])
        deciphered_message = rsa.decrypt(deciphered_message, private_key)
        return "Message déchiffré et ajouté aux journaux"
    else:
        return deciphered_message


if __name__ == '__main__':
    app.run()
