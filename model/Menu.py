class OpcjeMenu:

    def __init__(self) :
        self.__opcje = []
        self.__znaczniki = []

    def dodajOpcje(self, opcja):
        if not type(opcja) is Opcja :
            raise ValueError('Podana opcja nie jest klasą Opcja!')
        self.__opcje.append(opcja)
        self.__znaczniki.append(opcja.znacznik())

    def uruchomOpcjeZnacznika(self, znacznik):
        indeks = self.__indeksZnacznika(znacznik=znacznik)
        self.__opcje[indeks].funkcja()

    def czyWybranoPrawidlowyZnacznik(self, znacznik):
        return znacznik in self.__znaczniki

    def usunOpcje(self, znacznik):
        if self.czyWybranoPrawidlowyZnacznik(znacznik) :
            indeks = self.__indeksZnacznika(znacznik=znacznik)
            del self.__opcje[indeks]
            del self.__znaczniki[indeks]

    def zastapOpcje(self, opcja) :
        self.__czyArgumentJestTypuOpcja(opcja)
        self.usunOpcje(opcja.znacznik())
        self.dodajOpcje(opcja)

    def __czyArgumentJestTypuOpcja(self, opcja):
        if not type(opcja) is Opcja :
            raise ValueError('Podana opcja nie jest klasą Opcja!')

    def __indeksZnacznika(self, znacznik):
        return self.__znaczniki.index(znacznik)

    def __str__(self):
        s = ''
        for i in range(len(self.__opcje)) :
            s += str(self.__opcje[len(self.__opcje) - 1 - i])
        return s

class Opcja :

    def __init__(self, znacznik, opis, funkcja):
        self.__znacznik = znacznik.upper()
        self.__opis = opis
        self.__funkcja = funkcja

    def znacznik(self):
        return self.__znacznik

    def opis(self):
        return self.__opis

    def funkcja(self):
        self.__funkcja()

    def __str__(self):
        return ('%s - %s\n' % (self.__znacznik, self.__opis))