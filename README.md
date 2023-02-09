# small-keylogger
A small and simple keylogger written in Python. For educational purposes only.
  
The server generates a RSA keypair and awaits for a client to execute keylogger.py.
The client will then request the public key of RSA and encrypt each message with that key.

Each message is encoded into base64 and read by the server that way.

The keylogger needs improvement but it is a good starting point.
