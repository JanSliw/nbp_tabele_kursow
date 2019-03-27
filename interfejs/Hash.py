

def sha256(tekst):
    from hashlib import sha256
    return sha256(tekst.encode('utf-8')).hexdigest()

