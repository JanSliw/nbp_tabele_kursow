# uwaga: progrm manipuluje użytkownikami oraz ich dostępami do BD
# moduł instalacyjny z tworzeniem folderów i użytkowników na bazie
# polityka haseł - czy nie wystąpiło to hasło ostatnio, duże, małe znaki, specjalne, litery
# zrobić porządek w interfejsach - za dużo małych plików
# ----- dodawanie/usuwanie/modyfikacja userów - zrobione
# ----- odzyskiwanie haseł - admin może zmienić hasło
# ----- cofnąć wszystkim uprawnienia do tabel - dodać na wyszystko procedury z przedrostkiem a_ dla dmina i u_ dla admina i usera
# ----- utworzyć widoki w bazie danych z selektów
# ----- zmiana hasła w menu głównym i w menu zarządzania uzytkownikami
# zmiana typu usera na admina/usera
# sprawdzenie połączenia z internetem
# obsługa tabel innych niż A
# obsługa świąt NBP - patrz 2005


def run():
    from controller.Aplikacja import Aplikacja
    from sekret.Auth import poswiadczeniaTestAdmin
    from sekret.Auth import poswiadczeniaTestUser

    # a = Aplikacja()
    a = Aplikacja(poswiadczeniaTestAdmin)
    # a = Aplikacja(poswiadczeniaTestUser)
    print('Koniec programu.')

run()
