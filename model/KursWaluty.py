class KursWaluty :

    def __init__(self) :
        self.__nazwa = ''
        self.__przelicznik = 0
        self.__kod = ''
        self.__kurs = 0.0

    def utworz(self, nazwaWaluty, przelicznik, kodWaluty, kurs) :
        self.__nazwa = nazwaWaluty
        self.__przelicznik = int(przelicznik)
        self.__kod = kodWaluty
        if type(kurs) is str:
            self.__kurs = float(kurs.replace(',', '.'))
        else:
            self.__kurs = float(kurs)

    def czyZaczytanoWszyskieWartosci(self):
        if (self.__nazwa == ''
            or self.__przelicznik== 0
            or self.__kod == ''
            or self.__kurs == 0.0) :
            return 0
        else :
            return 1

    def nazwa(self) :
        return self.__nazwa

    def przelicznik(self) :
        return self.__przelicznik

    def kod(self) :
        return self.__kod

    def kurs(self) :
        return self.__kurs

    def __str__(self) :
        return '%5s | %10i | %7.4f | %s' % (self.__kod, self.__przelicznik, self.__kurs, self.__nazwa)

    def __eq__(self, other):
        if self.__nazwa == other.nazwa() and self.__kod == other.kod() :
            return True
        else :
            return False
