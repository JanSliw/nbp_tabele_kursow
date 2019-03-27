
from controller.Menu import Menu, Wejscie
from model.Menu import OpcjeMenu, Opcja
from controller.DB import DB

class Aplikacja :

    def __init__(self, poswiadczenia=None) :
        from controller.DB import DB
        self.__powitanie()
        db = DB(poswiadczenia)
        if db.czyLogowanieDoDBUdane():
            self.__admin = db.admin()
            print('Logowanie udane.')
            self.__wystwietlMenu()

    def __powitanie(self):
        print('Dzień dobry.')

    def __wystwietlMenu(self):
        print('Witaj user: %s' % DB.poswiadczenia.user())
        if self.__admin :
            m = MenuGlowneAdmin()
        else:
            m = MenuGlowne()
        m.wlaczMenu()



class MenuGlowne(Menu) :

    def __init__(self):
        Menu.__init__(self)
        self.__dodajOpcje()
        OpcjeMenu.usunOpcje(self, znacznik='P')

    def __dodajOpcje(self):
        o = Opcja(znacznik='H', opis='Zmiana hasła', funkcja=self.__zmianaHaslaMenu)
        Menu.dodajOpcje(self, o)
        o = Opcja(znacznik='K', opis='Kursy walut NBP', funkcja=self.__kursyWalutMenu)
        Menu.dodajOpcje(self, o)

    def wlaczMenu(self):
        Menu.wlaczMenu(self)
        self.__wyjscieZProgramu()

    def __kursyWalutMenu(self):
        m = KursyWalutMenu()
        self.pokazMenuPodrzedne(m)

    def __zmianaHaslaMenu(self):
        haslo = self.__pobierzHaslo()
        if self.czyPowrotZWejsciaLubKonczymy() :
            return
        DB().zmienHasloUzytkownikowi(haslo=haslo)
        print('Twoje hasło zostało zmienione.')

    def __pobierzHaslo(self):
        haslo = input('Podaj hasło: ')
        h = Wejscie(pytanie='Podaj ponownie hasło: ', funkcjaSprawdzajaca=self.__czyPodanoPoprawneHaslo, haslo=haslo)
        return self.wartoscZWejscia(h)

    def __czyPodanoPoprawneHaslo(self, hasloPowtorzone, haslo):
        if hasloPowtorzone == haslo :
            return True
        else :
            print("Podane hasła są niezgodne.")
            return False

    def __wyjscieZProgramu(self):
        print('Nastąpi wyjście z programu.')

class MenuGlowneAdmin(MenuGlowne) :

    def __init__(self,):
        MenuGlowne.__init__(self)
        self.__dodajOpcje()

    def __dodajOpcje(self):
        o = Opcja(znacznik='U', opis='Zarządzaj użytkownkami', funkcja=self.__zarzadzanieUzytkownikamiMenu)
        Menu.dodajOpcje(self, o)
        o = Opcja(znacznik='K', opis='Kursy walut NBP', funkcja=self.__kursyWalutMenuAdmin)
        Menu.zastapOpcje(self, o)

    def __zarzadzanieUzytkownikamiMenu(self):
        m = ZarzadzanieUzytkownikamiMenu()
        self.pokazMenuPodrzedne(m)

    def __kursyWalutMenuAdmin(self):
        m = KursyWalutMenuAdmin()
        self.pokazMenuPodrzedne(m)


class KursyWalutMenu(Menu) :

    def __init__(self):
        from controller.Dane import TabelaKursowController
        from controller.Plik import XmlNBP
        Menu.__init__(self)
        self. __LIMIT_DNI_WYSWIETLANYCH_W_TABELI_ARCHIWALNEJ = 5
        self.__dodajOpcje()
        self.__xmlNbp = XmlNBP()
        self.__tabelaKursowController = TabelaKursowController()

    def __dodajOpcje(self):
        o = Opcja(znacznik='O', opis='Ostatnia tabela kursów', funkcja=self.__ostatniaTabelaKursow)
        Menu.dodajOpcje(self, o)
        o = Opcja(znacznik='A', opis='Archiwalna tabela kursów', funkcja=self.__archiwalnaTabelaKursow)
        Menu.dodajOpcje(self, o)
        o = Opcja(znacznik='R', opis='Raporty', funkcja=self.__raportyMenu)
        Menu.dodajOpcje(self, o)

    def __ostatniaTabelaKursow(self):
        self.__xmlNbp.pobierzOstatniaTabeleKursowZNBP()
        xmlPlik = self.__xmlNbp.ostatnioPobranyPlik()
        self.__tabelaKursowController.pobierzZPlikuXml(xmlPlik)
        print(self.__tabelaKursowController)

    def __archiwalnaTabelaKursow(self):
        self.__wyswietlOstatnieNazwyPlikow()
        dataLubID = self.__pobierzDateLubID()
        if self.czyPowrotZWejsciaLubKonczymy() :
            return
        self.__pobierzDateINazwe(dataLubID)
        self.__pobierzZDBLubInternetuPoDacieLubNazwie()
        print(self.__tabelaKursowController)

    def __wyswietlOstatnieNazwyPlikow(self):
        dniTygodnia = {0: 'poniedziałek', 1: 'wtorek', 2: 'środa', 3: 'czwartek', 4: 'piątek'}
        z = "CALL u_ostatnie_nazwy_plikow(%i, DATE(SYSDATE()))" % self.__LIMIT_DNI_WYSWIETLANYCH_W_TABELI_ARCHIWALNEJ
        self.__lista = DB().zapytanie(z)
        print("%2s | %10s | %13s | %11s" % ('ID', 'DATA', 'DZIEN TYGODNIA', 'NAZWA PLIKU'))
        for w in range(len(self.__lista)) :
            print("%2i | %10s | %13s | %11s" % (self.__lista[w][0], self.__lista[w][1], dniTygodnia[self.__lista[w][2]], self.__lista[w][3]))

    def __pobierzDateLubID(self):
        u = Wejscie(pytanie='Podaj ID jednego z powyższych dni lub datę w formacie RRRR-MM-DD: ', funkcjaSprawdzajaca=self.__sprawdzPodanaDateLubIDIUstawNazwePliku)
        return self.wartoscZWejscia(u)

    def __sprawdzPodanaDateLubIDIUstawNazwePliku(self, dataLubID):
        from interfejs.RegExp import czySameCyfry
        from interfejs.RegExp import czyDataWFormacieYYYY_MM_DD

        wynik = False
        if czySameCyfry(dataLubID):
            if int(dataLubID) <= self.__LIMIT_DNI_WYSWIETLANYCH_W_TABELI_ARCHIWALNEJ and int(dataLubID) >= 0 :
                wynik = True
        elif czyDataWFormacieYYYY_MM_DD(dataLubID) :
            wynik = True

        if wynik == False :
            print("Podana wartosć jest nieprawidłowa.")

        return wynik

    def __nazwaPlikuZDaty(self, data):
        z = "SELECT u_nazwa_pliku_xml(STR_TO_DATE('" + data + "', '%Y-%m-%d'))"
        return DB().zapytanie(z)[0][0]

    def __pobierzDateINazwe(self, dataLubID):
        from interfejs.RegExp import czySameCyfry
        if czySameCyfry(dataLubID):
            id = int(dataLubID)
            self.__data = self.__lista[id][1]
            self.__nazwaPliku = self.__lista[id][3]
        else:
            self.__data = dataLubID
            self.__nazwaPliku = self.__nazwaPlikuZDaty(self.__data)
        self.__lista = None

    def __pobierzZDBLubInternetuPoDacieLubNazwie(self):
        if self.__tabelaKursowController.czyTabelaWystepujeWDBPoDacie(self.__data) :
            self.__tabelaKursowController.pobierzZDBPoDacie(self.__data)
        else :
            self.__xmlNbp.pobierzTabeleKursowZNBPPoNazwie(self.__nazwaPliku)
            xmlPlik = self.__xmlNbp.ostatnioPobranyPlik()
            self.__tabelaKursowController.pobierzZPlikuXml(xmlPlik)

    def __raportyMenu(self):
        print('Menu reportów!!!')



class KursyWalutMenuAdmin(KursyWalutMenu) :

    def __init__(self):
        KursyWalutMenu.__init__(self)
        self.__dodajOpcje()

    def __dodajOpcje(self):
        o = Opcja(znacznik='U', opis='Usuń wszystkie tabele z kursami walut', funkcja=self.__usunWszystkieTabele)
        Menu.dodajOpcje(self, o)
        o = Opcja(znacznik='S', opis='Ściągnij wszystkie tabele z kursami walut', funkcja=self.__sciagnijWszystkieTabele)
        Menu.dodajOpcje(self, o)

    def __usunWszystkieTabele(self):
        u = input("Czy chcesz usunąć wszystkie tabele z kursami walut? (T - tak, dowolny przycisk - nie ): ").upper()
        if u == 'T' :
            n = input("Na pewno? (T - tak, dowolny przycisk - nie ): ").upper()
            if n == 'T':
                z = "CALL a_usun_wszystkie_tabele()"
                DB().wykonaj(z)
                print("Wszystkie tabele z kursami usunięte")

    def __sciagnijWszystkieTabele(self):
        s = input("Czy chcesz teraz pobrać wszystkie tabele z kursami walut ze strony NBP? (T - tak, dowolny przycisk - nie ): ").upper()
        if s == 'T' :
            self.__pobierzWszystkieTabele()

    def __pobierzWszystkieTabele(self):

        z = "CALL u_ostatnie_nazwy_plikow(20000, SYSDATE())"
        self.__nazwyPlikow = DB().zapytanie(z)
        # self.__nazwyPlikow = DB().zapytanie(z)[:,3]
        self.__sciagnijZNBP()

    def __sciagnijZNBPIZapiszZFolderowDoDB(self):
        self.__sciagnijZNBP()
        self.__zapiszZFolderowDoDB()

    def __sciagnijZNBP(self):
        from controller.Plik import XmlNBP
        from urllib.error import HTTPError
        xmlNbp = XmlNBP()
        print("Rozpoczynam pobieranie plików")
        for w in range(len(self.__nazwyPlikow)):
            self.__nazwaPliku = self.__nazwyPlikow[w][3]
            # self.__nazwaPliku = self.__nazwyPlikow[w]
            while True :
                try :
                    xmlNbp.pobierzTabeleKursowZNBPPoNazwie(self.__nazwaPliku)
                    print("Plik %s został pobrany." % self.__nazwaPliku)
                    break
                except HTTPError as e:
                    if e.code == 404 :
                        break
        self.__foldery = xmlNbp.ostatnieKatalogiZPobranymiPlikami()
        print("Wszystkie pliki zostały pobrane.")

    def __zapiszZFolderowDoDB(self):
        from controller.Dane import TabelaKursowController
        tabelaKursowController = TabelaKursowController()
        print("Rozpoczynam pobieranie plików do bazy danych")
        for f in self.__foldery :
            print("Pobieranie danych z folderu: " + f)
            tabelaKursowController.pobierzZKataloguDoDB(sciezka=f)
        print("Wszyskie pliki zostały wczytane do bazy danych")




class ZarzadzanieUzytkownikamiMenu(Menu) :

    def __init__(self):
        Menu.__init__(self)
        self.__dodajOpcje()

    def __dodajOpcje(self):
        o = Opcja(znacznik='U', opis='Usuń użytkownika', funkcja=self.__usunUzytkownika)
        Menu.dodajOpcje(self, o)
        o = Opcja(znacznik='Z', opis='Zmień hasło użytkownika', funkcja=self.__zmienHasloUzytkownika)
        Menu.dodajOpcje(self, o)
        o = Opcja(znacznik='D', opis='Dodaj użytkownika', funkcja=self.__dodajUzytkownika)
        Menu.dodajOpcje(self, o)

    def __dodajUzytkownika(self):
        user = self.__pobierzNazweNowegoUzytkownika()
        if self.czyPowrotZWejsciaLubKonczymy() :
            return
        haslo = self.__pobierzHaslo()
        if self.czyPowrotZWejsciaLubKonczymy() :
            return
        a = input("Czy użytkownik ma być adminem? (T - tak, dowolny przycisk - nie ): ").upper()
        admin = 'A' if a == 'T' else 'U'
        DB().dodajUzytkownika(uzytkownik=user, haslo=haslo, admin=admin)
        print('Użytkownik %s został dodany.' % user)

    def __pobierzNazweNowegoUzytkownika(self):
        u = Wejscie(pytanie='Podaj nazwę użytkownika, którego chcesz dodać (maksymalnie 50 znaków, tylko łacińskie litery): ', funkcjaSprawdzajaca=self.__sprawdzPodanegoNowegoUzytkownika)
        return self.wartoscZWejscia(u)

    def __sprawdzPodanegoNowegoUzytkownika(self, user):
        from interfejs.RegExp import czyTylkoMaleLiteryBezDiakrytycznych
        wynik = False
        user = user.lower()
        if len(user) > 50:
            print("Podany login ma więcej niż 50 znaków.")
        elif (not czyTylkoMaleLiteryBezDiakrytycznych(tekst=user)):
            print("Podany login zawiera niedozwolone znaki. Login może zawierać jedynie łacińskie litery.")
        elif DB().czyUzytkownikIstnieje(uzytkownik=user) :
            u = input("Podany użytkownik istnieje. \nChcesz go usunąć i stworzyć nowego użytkownika? (T - tak, dowolny przycisk - nie ): ").upper()
            if u == "T" :
                wynik = True
        else:
            wynik = True
        return wynik

    def __pobierzHaslo(self):
        haslo = input('Podaj hasło: ')
        h = Wejscie(pytanie='Podaj ponownie hasło: ', funkcjaSprawdzajaca=self.__czyPodanoPoprawneHaslo, haslo=haslo)
        return self.wartoscZWejscia(h)

    def __czyPodanoPoprawneHaslo(self, hasloPowtorzone, haslo):
        if hasloPowtorzone == haslo :
            return True
        else :
            print("Podane hasła są niezgodne.")
            return False

    def __usunUzytkownika(self):
        self.__pokazUzytkownikowDoUsuniecia()
        user = self.__pobierzNazweUzytkownika()
        if self.czyPowrotZWejsciaLubKonczymy() :
            return
        DB().usunUzytkownika(uzytkownik=user)
        print('Użytkownik %s został usunięty.' % user)

    def __pokazUzytkownikowDoUsuniecia(self):
        print('Lista wszystkich uzytkowników do usunięcia:')
        lista = DB().listaUzytkownikowBezZalogowanego()
        self.__wyswietlListeUzytkownikow(lista)

    def __wyswietlListeUzytkownikow(self, lista):
        print("%20s | %15s | %13s" % ('NAZWA', 'DATA_UTWORZENIA', 'TYP_UZYTKOWNIKA'))
        for w in range(len(lista)) :
            print("%20s | %15s | %13s" % (lista[w][0], lista[w][1], lista[w][2]))

    def __pobierzNazweUzytkownika(self):
        u = Wejscie(pytanie='Podaj nazwę użytkownika: ', funkcjaSprawdzajaca=self.__sprawdzPodanegoUzytkownika)
        return self.wartoscZWejscia(u)

    def __sprawdzPodanegoUzytkownika(self, user):
        user = user.lower()
        if DB().czyUzytkownikIstnieje(uzytkownik=user) :
            wynik = True
        else:
            print('Podany użytkownik nie istnieje.')
            wynik = False
        return wynik

    def __pokazWszystkichUzytkownikow(self):
        print('Lista wszystkich uzytkowników:')
        lista = DB().listaUzytkownikow()
        self.__wyswietlListeUzytkownikow(lista)

    def __zmienHasloUzytkownika(self):
        self.__pokazWszystkichUzytkownikow()
        user = self.__pobierzNazweUzytkownika()
        if self.czyPowrotZWejsciaLubKonczymy() :
            return
        haslo = self.__pobierzHaslo()
        if self.czyPowrotZWejsciaLubKonczymy() :
            return
        DB().zmienHasloUzytkownikowi(haslo=haslo, uzytkownik=user)
        print('Hasło użytkownika %s zostało zmienione.' % user)
