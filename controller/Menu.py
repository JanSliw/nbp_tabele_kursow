from model.Menu import OpcjeMenu, Opcja

class Menu(OpcjeMenu) :

    def __init__(self):
        OpcjeMenu.__init__(self)
        self.wyjscie = 0
        self.__powrot = 0
        self.__wejscie = Wejscie()
        self.__dodajOpcjeWyjscia()

    def __wybranoZnacznik(self, znacznik):
        if OpcjeMenu.czyWybranoPrawidlowyZnacznik(self, znacznik=znacznik) :
            OpcjeMenu.uruchomOpcjeZnacznika(self, znacznik=znacznik)
        else :
            self.__niepoprawnaOpcja()

    def wlaczMenu(self):
        czekamyNaWyjscieZMenu = True
        while czekamyNaWyjscieZMenu :
            s = self.__str__()
            self.__uzyskajPrawidlowyZnacznik(s)
            if self.czyKonczymy():
                czekamyNaWyjscieZMenu = False

    def __uzyskajPrawidlowyZnacznik(self, s):
        czekamyNaPrawidlowyZnacznik = True
        while czekamyNaPrawidlowyZnacznik:
            znacznik = input(s).upper()
            self.__wybranoZnacznik(znacznik=znacznik)
            if OpcjeMenu.czyWybranoPrawidlowyZnacznik(self, znacznik=znacznik):
                czekamyNaPrawidlowyZnacznik = False

    def czyKonczymy(self):
        return (self.wyjscie + self.__powrot > 0)


    def pokazMenuPodrzedne(self, menuPodrzedne) :
        menuPodrzedne.wlaczMenu()
        self.wyjscie = menuPodrzedne.wyjscie

    def __ustawWejscie(self, wejscie):
        self.__wejscie = wejscie
        self.__przygotujDoWyjsciaJezeliNaWejsciuNieMaPrawidlowejWartosci()

    def wartoscZWejscia(self, wejscie):
        self.__ustawWejscie(wejscie)
        return self.wejscie().wartosc()

    def __przygotujDoWyjsciaJezeliNaWejsciuNieMaPrawidlowejWartosci(self):
        if not self.__wejscie.czyOtrzymanoPoprawnaWartosc() :
            self.wyjscie = self.__wejscie.wyjscie()

    def wejscie(self):
        return self.__wejscie

    def czyPowrotZWejsciaLubKonczymy(self):
        return (self.wyjscie + self.__powrot + self.__wejscie.powrot() > 0)

    def __powrotWybrany(self):
        self.__powrot = 1

    def __wyjscieWybrane(self):
        self.wyjscie = 1

    def __dodajOpcjeWyjscia(self):
        o = Opcja('Q', 'Wyjscie', self.__wyjscieWybrane)
        self.dodajOpcje(o)
        o = Opcja('P', 'Powrót do poprzedniego menu', self.__powrotWybrany)
        self.dodajOpcje(o)

    def __niepoprawnaOpcja(self):
        print('Wybrałeś niepoprawną opcję. Spróbuj jeszcze raz.')

    def __str__(self):
        s = '\nWybierz jedną z poniższych opcji:\n'
        s += OpcjeMenu.__str__(self)
        return s


class Wejscie():

    def __init__(self, pytanie='', funkcjaSprawdzajaca=None, **kwargs):
        self.__wyjscie = 0
        self.__powrot = 0
        if pytanie == '' :
            return
        self.__pytanie = pytanie
        self.__funkcjaSprawdzajaca = funkcjaSprawdzajaca
        self.__wartosc = ''
        self.__wartoscPrawidlowa = False
        self.__zadajPytanieISprawdzWartosc(**kwargs)

    def __zadajPytanieISprawdzWartosc(self, **kwargs):
        czekamyNaPrawidlowaWartosc = True
        while czekamyNaPrawidlowaWartosc :
            self.__wartosc = input(self.__pytanie)
            self.__sprawdzWartosc(**kwargs)
            if self.__wartoscPrawidlowa :
                czekamyNaPrawidlowaWartosc = False
            else :
                m = SprobujPonownieMenu()
                m.wlaczMenu()
                self.__wyjscie = m.wyjscie
                if m.czyKonczymy() :
                    self.__powrot = 1
                    czekamyNaPrawidlowaWartosc = False

    def __sprawdzWartosc(self, **kwargs):
        self.__wartoscPrawidlowa = self.__funkcjaSprawdzajaca(self.__wartosc, **kwargs)

    def wartosc(self):
        if self.czyOtrzymanoPoprawnaWartosc() :
            return self.__wartosc

    def czyOtrzymanoPoprawnaWartosc(self):
        return self.__wartoscPrawidlowa

    def wyjscie(self):
        return self.__wyjscie

    def powrot(self):
        return self.__powrot


class SprobujPonownieMenu(Menu) :

    def __init__(self):
        Menu.__init__(self)
        self.__dodajOpcje()
        self.__probujPonownie = 0

    def __dodajOpcje(self):
        o = Opcja(znacznik='S', opis='Spróbuj ponownie', funkcja=self.__sprobujPonownie)
        Menu.dodajOpcje(self, o)

    def wlaczMenu(self):
        Menu.wlaczMenu(self)
        if self.__probujPonownie == 1:
            self.wyjscie = 0

    def __sprobujPonownie(self):
        self.__probujPonownie = 1
        self.wyjscie = 1
