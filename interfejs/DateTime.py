

def data(rok, miesiac, dzien):
    from datetime import date
    return date(rok, miesiac, dzien)


def pobierzDateZTekstuYYYY_MM_DD(tekst):
    from datetime import datetime
    return datetime.strptime(tekst, '%Y-%m-%d')


def formatujDateDoTekstuYYYY_MM_DD(data):
    return data.strftime('%Y-%m-%d')

