class TabelaKursow:

    def __init__(self) :
        from interfejs.DateTime import data
        self.__kursy = []
        self.__typ = ''
        self.__uid = ''
        self.__numer = ''
        self.__dataPubl = data(rok=1, miesiac=1, dzien=1)
        self.__dataPublTekst = ''
        self.__KLUCZE = {1:'Nazwa', 2:'Kod waluty'}

    def utworz(self, typ_tabeli, uid_tabeli, numer_tabeli, data_publikacji) :
        from interfejs.DateTime import pobierzDateZTekstuYYYY_MM_DD, formatujDateDoTekstuYYYY_MM_DD
        self.__typ = typ_tabeli
        self.__uid = uid_tabeli
        self.__numer = numer_tabeli
        if type(data_publikacji) is str:
            self.__dataPubl =  pobierzDateZTekstuYYYY_MM_DD(data_publikacji)
            self.__dataPublTekst = data_publikacji
        else :
            self.__dataPubl = data_publikacji
            self.__dataPublTekst = formatujDateDoTekstuYYYY_MM_DD(data_publikacji)

    def typ(self) :
        return self.__typ

    def uid(self) :
        return self.__uid

    def numer(self) :
        return self.__numer

    def dataPubl(self) :
        return self.__dataPubl

    def dataPublTekst(self):
        return self.__dataPublTekst

    def dodajLubZastapKurs(self, kursWaluty):
        self.__usunKursWaluty(kursWaluty)
        self.__kursy.append(kursWaluty)

    def __usunKursWaluty(self, kursWaluty):
        for k in self.__kursy :
            if k == kursWaluty :
                self.__kursy.remove(k)

    def znajdzKurs(self, szukanaWartosc, klucz):
        if not self.__kluczZnajdujeSieWKluczach(klucz=klucz) :
            raise ValueError("znajdzKurs: klucz musi być jedną z następujących wartości %r." % self.__KLUCZE)
        if klucz == 1 :
            return self.__znajdzKursPoNazwie(szukanaWartosc=szukanaWartosc)
        else :
            return self.__znajdzKursPoKodzie(szukanaWartosc=szukanaWartosc)

    def czyZaczytanoWszyskieWartosci(self):
        if (self.__typ == ''
            or self.__dataPublTekst == ''
            or self.__numer == ''
            or self.__uid == ''
            or len(self.__kursy) == 0) :
            return 0
        else :
            return 1

    def kursy(self):
        return self.__kursy

    def __kluczZnajdujeSieWKluczach(self, klucz) :
        return klucz in self.__KLUCZE

    def __znajdzKursPoNazwie(self, szukanaWartosc) :
        for k in self.__kursy :
            if k.nazwa() == szukanaWartosc :
                return k
        raise ValueError('znajdzKurs: nie istnieje kurs waluty, który w polu "Nazwa" ma podaną wartosc "%s".' % szukanaWartosc +
                         'wybierz jedną z poniższych \n' + self.__nazwyWalut())

    def __znajdzKursPoKodzie(self, szukanaWartosc):
        for k in self.__kursy:
            if k.kod() == szukanaWartosc:
                return k
        raise ValueError('znajdzKurs: nie istnieje kurs waluty, który w polu "Kod waluty" ma podaną wartosc "%s".' % szukanaWartosc +
                         'wybierz jedną z poniższych \n' + self.__kodyWalut())

    def __nazwyWalut(self) :
        s = ''
        for k in self.__kursy :
            s = s + '* %s \n' % k.nazwa()
        return s

    def __kodyWalut(self):
        s = ''
        for k in self.__kursy:
            s = s + '* %s \n' % k.kod()
        return s

    def __str__(self):
        s = '\n****** Tabela ******\n'
        s = s + 'Numer tabeli: %s \n' % self.__numer
        s = s + 'Data publikacji: %s \n' % self.__dataPublTekst
        s = s + '%5s | %10s| %7s | %s\n' % ('KOD', 'PRZELICZNIK', 'KURS', 'NAZWA WALUTY')
        for k in self.__kursy :
            s = s + str(k) + '\n'
        return s
