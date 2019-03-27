from model.TabelaKursow import TabelaKursow
from controller.DB import DB

class TabelaKursowController(TabelaKursow) :

    def __init__(self):
        TabelaKursow.__init__(self)

    def pobierzZPlikuXml(self, sciezka) :
        self.__zPlikuDoModelu(sciezka)
        self.zapiszDoDB()

    def __zPlikuDoModelu(self, sciezka):
        from interfejs.XmlParser import dokumentZeSciezki
        from interfejs.XmlParser import pobierzAtrybutZElementu
        from interfejs.XmlParser import zbierzDaneZPierwszegoDzieckaZElementuPoTagu
        from interfejs.XmlParser import wybierzDzieciZElementuPoTagu

        dok = dokumentZeSciezki(sciezka=sciezka)
        typ = pobierzAtrybutZElementu(atrybut='typ', element=dok)
        uid = pobierzAtrybutZElementu(atrybut='uid', element=dok)
        numer = zbierzDaneZPierwszegoDzieckaZElementuPoTagu(element=dok, tag='numer_tabeli')
        dataPublikacji = zbierzDaneZPierwszegoDzieckaZElementuPoTagu(element=dok, tag='data_publikacji')
        self.utworz(typ_tabeli=typ, uid_tabeli=uid, numer_tabeli=numer, data_publikacji=dataPublikacji)
        self.__zbierzWalutyZElementowDom(wybierzDzieciZElementuPoTagu(element=dok, tag='pozycja'))

    def __zbierzWalutyZElementowDom(self, elementyDom) :
        for e in elementyDom :
            kurs = KursWalutyController()
            kurs.pobierzZElementuDom(elementDom=e)
            self.dodajLubZastapKurs(kursWaluty=kurs)

    def zapiszDoDB(self, db = None):
        if not self.czyZaczytanoWszyskieWartosci() :
            return
        z = ("CALL u_dodaj_tabele_kursow('%s', STR_TO_DATE('%s', '%%Y-%%m-%%d'), '%s', '%s')"
             % (self.numer(), self.dataPublTekst(), self.uid(), self.typ()))
        if db == None :
            db = DB()
        db.wykonaj(z)
        db.commituj()
        for k in self.kursy() :
            k.zapiszDoDB(numer_tabeli=self.numer())

    def pobierzZKataloguDoDB(self, sciezka):
        from interfejs.Os import listaWszystkichPlikowWKatalogu
        lista = listaWszystkichPlikowWKatalogu(sciezka)
        self.pobierzZListyPlikowDoDB(lista)

    def pobierzZListyPlikowDoDB(self, lista):
        db = DB()
        for p in lista:
            self.__zPlikuDoModelu(sciezka=p)
            self.zapiszDoDB(db)

    def czyTabelaWystepujeWDBPoDacie(self, data):
        z = ("SELECT COUNT(1) " +
             "FROM u_tabela_z_kursami " +
             "WHERE data = STR_TO_DATE('" + data + "', '%Y-%m-%d')")
        return DB().zapytanie(z)[0][0]

    def pobierzZDBPoDacie(self, data):
        z = ("SELECT numer, data, uid, typ " +
             "FROM u_tabela_z_kursami " +
             "WHERE data = STR_TO_DATE('" + data + "', '%Y-%m-%d')")
        db = DB()
        wynik = db.zapytanie(z)
        self.utworz(numer_tabeli=wynik[0][0], data_publikacji=wynik[0][1],uid_tabeli=wynik[0][2] , typ_tabeli=wynik[0][3])
        z = ("CALL u_kursy_z_tabeli('%s')" % wynik[0][0])
        wynik = db.zapytanie(z)
        self.__pobierzWalutyZListy(wynik)

    def __pobierzWalutyZListy(self, lista):
        for w in lista :
            kurs = KursWalutyController()
            kurs.utworz(nazwaWaluty=w[0], przelicznik=w[1], kodWaluty=w[2], kurs=w[3])
            self.dodajLubZastapKurs(kursWaluty=kurs)


from model.KursWaluty import KursWaluty

class KursWalutyController(KursWaluty) :

    def __init__(self):
        KursWaluty.__init__(self)

    def pobierzZElementuDom(self, elementDom) :
        from interfejs.XmlParser import zbierzDaneZPierwszegoDzieckaZElementuPoTagu
        nazwa = zbierzDaneZPierwszegoDzieckaZElementuPoTagu(element=elementDom, tag='nazwa_waluty')
        przelicznik= zbierzDaneZPierwszegoDzieckaZElementuPoTagu(element=elementDom, tag='przelicznik')
        kod = zbierzDaneZPierwszegoDzieckaZElementuPoTagu(element=elementDom, tag='kod_waluty')
        kurs = zbierzDaneZPierwszegoDzieckaZElementuPoTagu(element=elementDom, tag='kurs_sredni')
        self.utworz(nazwaWaluty=nazwa,  przelicznik=przelicznik, kodWaluty=kod, kurs=kurs)

    def zapiszDoDB(self, numer_tabeli) :
        if not self.czyZaczytanoWszyskieWartosci() :
            return
        z = ("CALL u_dodaj_kurs('%s', '%s', '%s', %i, %16.6f)"
              % (self.nazwa(), self.kod(), numer_tabeli, self.przelicznik(), self.kurs()))
        db = DB()
        db.wykonaj(z)
        db.commituj()



