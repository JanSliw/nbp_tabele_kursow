

def pobierzZUrlDoPliku(url, plik):
    import urllib.request as rq
    rq.urlretrieve(url, plik)

