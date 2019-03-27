
class Poswiadczenia:

    def __init__(self, user='logon', haslo='logon', zaszyfrowaneHaslo=False):
        from interfejs.Hash import sha256
        self.__user = user
        if zaszyfrowaneHaslo :
            self.__haslo= haslo
        else :
            self.__haslo = sha256(haslo)

    def user(self):
        return self.__user

    def haslo(self):
        return self.__haslo

class Conn:

    def __init__(self):
        from interfejs.MySql import MySql
        self.__MySQl = MySql()
        self.__poswiadczenia = Poswiadczenia()
        self.__admin = 0

    def polaczenie(self, poswiadczenia) :
        self.__poswiadczenia = poswiadczenia
        danePolaczenia = self.__zbierzDanePolaczenia()
        self.__MySQl.polaczenie(danePolaczenia=danePolaczenia)
        if self.__poswiadczenia.user() != 'logon' :
            self.__zalogujPrzezTabeleLoginy()
            self.__pobierzPoziomDostepu()

    def __zbierzDanePolaczenia(self):
        # sekretneDane zawiera słownik z danymi połączenia (co najmniej {'host':'x', 'db':'x'})
        from sekret.Auth import sekretneDane
        mniejSekretneDane = {'charset': 'utf8'}
        daneLogowania = {'user':self.__poswiadczenia.user(), 'password': self.__poswiadczenia.haslo()}
        return dict(**sekretneDane, **mniejSekretneDane, **daneLogowania)

    def __zalogujPrzezTabeleLoginy(self):
        z = ("SELECT u_sprawdz_login('%s', '%s')" % (self.__poswiadczenia.user(), self.__poswiadczenia.haslo()))
        if self.__MySQl.zapytanie(z)[0][0] != 1 :
            raise ValueError('Logowanie do aplikacji nie powiodło się.')
        z = ("CALL u_zapisz_sesje('%s')" % self.__poswiadczenia.user())
        self.__MySQl.procedura(z)
        self.commituj()

    def __pobierzPoziomDostepu(self):
        z = ("SELECT u_czy_admin('%s')" % (self.__poswiadczenia.user()))
        if self.__MySQl.zapytanie(z)[0][0] == 1 :
            self.__admin = 1

    def admin(self):
        return (self.__admin == 1)

    def zmienHasloUzytkownikowi(self, haslo, uzytkownik=''):
        from interfejs.Hash import sha256
        haslo = sha256(haslo)
        if self.admin() and len(uzytkownik) > 0 :
            user = uzytkownik
        else :
            user = self.__poswiadczenia.user()
        id = self.__idUzytkownika(uzytkownik=user)
        z = ("CALL u_nadaj_haslo(%i, '%s')" % (id, haslo))
        self.__wykonajICommituj(z)

    def dodajUzytkownika(self, uzytkownik, haslo, admin):
        from interfejs.Hash import sha256
        if self.admin() :
            haslo = sha256(haslo)
            z = ("CALL a_stworz_uzytkownika('%s', '%s', '%s')" % (uzytkownik, haslo, admin))
            self.__wykonajICommituj(z)

    def usunUzytkownika(self, uzytkownik):
        if self.admin() :
            z = ("CALL a_usun_uzytkownika('%s')" % uzytkownik)
            self.__wykonajICommituj(z)

    def czyUzytkownikIstnieje(self, uzytkownik):
        try :
            self.__idUzytkownika(uzytkownik)
        except ValueError :
            return False
        return True

    def zapytanie(self, komenda):
        return self.__MySQl.zapytanie(komenda)

    def listaUzytkownikow(self):
        return self.__zwrocListeUzytkownikow()

    def listaUzytkownikowBezZalogowanego(self):
        return self.__zwrocListeUzytkownikow(warunek=("WHERE nazwa <> '%s'" % self.__poswiadczenia.user()))

    def __wykonajICommituj(self, komenda):
        self.__MySQl.procedura(komenda)
        self.__MySQl.commit()

    def wykonaj(self, komenda):
        self.__MySQl.procedura(komenda)

    def commituj(self):
        self.__MySQl.commit()

    def __zwrocListeUzytkownikow(self, warunek=''):
        z = ("SELECT nazwa, data_utworzenia, admin " +
             "FROM a_uzytkownicy " +
              warunek)
        return self.zapytanie(z)

    def __idUzytkownika(self, uzytkownik):
        z = ("SELECT u_id_uzytkownika('%s')" % uzytkownik)
        id = self.__MySQl.zapytanie(z)[0][0]
        if id == None :
            raise ValueError('Użytkownik pod nazwą "' + uzytkownik + '" nie istnieje.')
        else :
            return id

    def zamknijPolaczenie(self):
        self.__MySQl.zamknijPolaczenie()


class DB(Conn) :

    poswiadczenia = Poswiadczenia()

    def __init__(self,  poswiadczenia=None):
        Conn.__init__(self)
        self.__limitProbLogowania = 3
        self.__admin = 0
        self.__zalogowano = 0

        if poswiadczenia == None :
            self.__czyPodanoPoswiadczeniaWKonstruktorze = 0
        else :
            DB.poswiadczenia = poswiadczenia
            self.__czyPodanoPoswiadczeniaWKonstruktorze = 1

        if self.__czyJuzZalogowany() == 1 :
            self.polaczenie(DB.poswiadczenia)
            self.__zakonczLogowanie()
        else :
            if DB.poswiadczenia.user() != 'logon' and poswiadczenia == None :
                print("Twoja sesja wygasła. Konieczne jest ponowne wprowadzenie poświadczeń.")
            self.__zaloguj()

    def __czyJuzZalogowany(self):
        if DB.poswiadczenia.user() == 'logon' :
            return 0
        else :
            poswiadczenia = Poswiadczenia(user='logon', haslo='logon', zaszyfrowaneHaslo=False)
            self.polaczenie(poswiadczenia)
            wynik = self.zapytanie("SELECT l_czy_zalogowany('%s')" % DB.poswiadczenia.user())[0][0]
            self.zamknijPolaczenie()
            return wynik

    def __zaloguj(self):
        if self.__czyPodanoPoswiadczeniaWKonstruktorze :
            self.__probaLogowania()
        else :
            self.__logowanie()

    def __logowanie(self) :
        for i in range(self.__limitProbLogowania):
            self.__zbierzPoswiadczeniaISprobujZalogowac()
            if self.czyLogowanieDoDBUdane() :
                return
            elif self.__limitProbLogowania > i + 1 :
                print('Spróbuj się ponownie zalogować. Zostało Ci %i prób.' % (self.__limitProbLogowania - i -1))
            else:
                from sys import exit as sysExit
                print('Przekroczono limit prób logowania. Program zostanie zamknięty.')
                sysExit()

    def __zbierzPoswiadczeniaISprobujZalogowac(self) :
        user = input('Podaj login: ')
        haslo = input('Podaj hasło: ')
        DB.poswiadczenia = Poswiadczenia(user, haslo, zaszyfrowaneHaslo=False)
        self.__probaLogowania()

    def __probaLogowania(self) :
        from interfejs.Time import czekaj
        if self.__czyPodanoPoswiadczeniaWKonstruktorze == 0 :
            czekaj(sekundy=1.5)
        try:
            self.polaczenie(DB.poswiadczenia)
            self.__zakonczLogowanie()
        except Exception as e:
            print(e)

    def czyLogowanieDoDBUdane(self):
        return self.__zalogowano

    def __zakonczLogowanie(self):
        self.__zalogowano = 1
        self.__admin = self.admin()



