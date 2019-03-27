import os.path as __path


def sciezkaSkryptu(sciezka=__file__):
    return __path.realpath(path=sciezka)


def folderNadrzednyDoSciezki(sciezka, powtorz=1):
    from os import pardir
    for i in range(powtorz):
        sciezka = __path.normpath(__path.join(sciezka, pardir))
    return sciezka


def czySciezkaInstnieje(sciezka):
    return __path.exists(sciezka)


def sprawdzCzyKatalogIstniejeIUtworz(sciezka):
    from os import makedirs
    if not czySciezkaInstnieje(sciezka=sciezka):
        makedirs(sciezka)


def usunZasobJezeliIsnieje(sciezka):
    from os import remove
    if czySciezkaInstnieje(sciezka=sciezka):
        remove(sciezka)

def listaWszystkichPlikowWKatalogu(sciezka) :
    from pathlib import Path
    wynik = []
    if czySciezkaInstnieje(sciezka):
        lista = Path(sciezka).glob('**/*')
        for p in lista:
            s = str(p)
            wynik.append(s)
    return wynik