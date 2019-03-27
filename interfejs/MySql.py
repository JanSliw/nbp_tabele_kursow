

class MySql:

    def __init__(self) :
        self.__conn = None

    def polaczenie(self, danePolaczenia) :
        from pymysql import connect
        try:
            self.__conn = connect(**danePolaczenia)
        except:
            raise ValueError('Podano błędne dane logowania do bazy danych!')

    def zapytanie(self, komenda) :
        kursor = self.__conn.cursor()
        kursor.execute(komenda)
        wynik = kursor.fetchall()
        kursor.close()
        return wynik

    def procedura(self, komenda) :
        kursor = self.__conn.cursor()
        kursor.execute(komenda)
        kursor.close()

    def zamknijPolaczenie(self) :
        self.__conn.close()

    def commit(self) :
        self.__conn.commit()

    def rollback(self):
        self.__conn.rollback()


