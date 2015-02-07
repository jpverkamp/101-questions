import random

ID_ALPHABET = 'abcdefghijklmnopqrstuvwxyz0123456789'
ID_LENGTH = 7

def randomID():
    return ''.join([random.choice(ID_ALPHABET) for i in range(ID_LENGTH)])
