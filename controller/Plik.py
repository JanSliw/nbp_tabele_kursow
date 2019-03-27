
class XmlNBP :

    def __init__(self) :
        self.__plik = Plik()
        self.__ostatnioPobrany = ''
        self.__urlNbp = 'http://www.nbp.pl/kursy/xml/'
        self.__pobraneFoldery = set()

    def pobierzTabeleKursowZNBPPoNazwie(self, nazwa):
        plik = self.__sciezkaPlikuXmlPoNazwie(nazwa)
        url = self.__urlNbp + nazwa + '.xml'
        self.__pobierzTabeleKursowNBPZUrlDoPliku(url=url, plik=plik)

    def __sciezkaPlikuXmlPoNazwie(self, nazwa) :
        self.__plik.ustawPlikXMl(nazwa)
        return self.__plik.sciezkaXml()

    def __pobierzTabeleKursowNBPZUrlDoPliku(self, url, plik):
        from interfejs.Url import pobierzZUrlDoPliku
        pobierzZUrlDoPliku(url=url, plik=plik)
        self.__ostatnioPobrany = plik
        self.__pobraneFoldery.add(self.__plik.katalogXml())

    def pobierzOstatniaTabeleKursowZNBP(self):
        self.pobierzTabeleKursowZNBPPoNazwie('LastA')

    def ostatnioPobranyPlik(self) :
        return self.__ostatnioPobrany

    def ostatnieKatalogiZPobranymiPlikami(self):
        return self.__pobraneFoldery



class Plik :

    def __init__(self) :
        self.__katalog = ''
        self.__sciezka = ''
        self.__sciezkaSkryptu = __file__

    def ustawPlikXMl(self, nazwaPlikuBezRozszerzenia):
        self.__ustawKatalogXml()
        if nazwaPlikuBezRozszerzenia[:5] == 'LastA' :
            self.__sciezka = self.__katalog + '\\' + nazwaPlikuBezRozszerzenia + '.xml'
        else :
            folder = str(2000 + int(nazwaPlikuBezRozszerzenia[-6:][:2]))
            self.__sciezka = self.__katalog + '\\' + folder + '\\' + nazwaPlikuBezRozszerzenia + '.xml'
            self.__ustawKatalog(folder)
        self.__usunXmlJezeliIstnieje()

    def __ustawKatalogXml(self) :
        katalogNadrzedny = self.__sciezkaKataloguNadrzednegoDoKataloguZrodlowegoSkryptu()
        self.__katalog = katalogNadrzedny + '\XML'
        self.__sprawdCzyKatalogIstniejeIUtworz()

    def __ustawKatalog(self, folder):
        self.__katalog += '\\' + folder
        self.__sprawdCzyKatalogIstniejeIUtworz()

    def __usunXmlJezeliIstnieje(self) :
        from interfejs.Os import usunZasobJezeliIsnieje
        usunZasobJezeliIsnieje(sciezka=self.__sciezka)

    def __sciezkaKataloguNadrzednegoDoKataloguZrodlowegoSkryptu(self) :
        from interfejs.Os import folderNadrzednyDoSciezki
        from interfejs.Os import sciezkaSkryptu
        sciezka = sciezkaSkryptu(sciezka=self.__sciezkaSkryptu)
        return folderNadrzednyDoSciezki(sciezka=sciezka, powtorz=2)

    def __sprawdCzyKatalogIstniejeIUtworz(self) :
        from interfejs.Os import sprawdzCzyKatalogIstniejeIUtworz
        sprawdzCzyKatalogIstniejeIUtworz(sciezka=self.__katalog)

    def sciezkaXml(self) :
        return self.__sciezka

    def katalogXml(self):
        return self.__katalog

