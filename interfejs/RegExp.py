

def czyTylkoMaleLiteryBezDiakrytycznych(tekst) :
    from re import search
    return search('[^a-z]+', tekst) == None

def czySameCyfry(tekst):
    from re import search
    return search("[^0-9]+", tekst) == None

def czyDataWFormacieYYYY_MM_DD(tekst) :
    from re import search
    return search("^(\d{4}\-(0?[1-9]|1[012])\-([12][0-9]|3[01]|0?[1-9]|)){1}$", tekst) != None

def testCzyTylkoMaleLitery() :
    s = 'aaa'
    print('"%s" daje wynik: %s' % (s, czyTylkoMaleLiteryBezDiakrytycznych(s)))
    s = 'aAaa'
    print('"%s" daje wynik: %s' % (s, czyTylkoMaleLiteryBezDiakrytycznych(s)))
    s = 'Aaa'
    print('"%s" daje wynik: %s' % (s, czyTylkoMaleLiteryBezDiakrytycznych(s)))
    s = 'aaaA'
    print('"%s" daje wynik: %s' % (s, czyTylkoMaleLiteryBezDiakrytycznych(s)))
    s = 'AAA'
    print('"%s" daje wynik: %s' % (s, czyTylkoMaleLiteryBezDiakrytycznych(s)))
    s = '1aa'
    print('"%s" daje wynik: %s' % (s, czyTylkoMaleLiteryBezDiakrytycznych(s)))
    s = 'aa1'
    print('"%s" daje wynik: %s' % (s, czyTylkoMaleLiteryBezDiakrytycznych(s)))
    s = 'a1a'
    print('"%s" daje wynik: %s' % (s, czyTylkoMaleLiteryBezDiakrytycznych(s)))
    s = '123'
    print('"%s" daje wynik: %s' % (s, czyTylkoMaleLiteryBezDiakrytycznych(s)))
    s = 'Ą'
    print('"%s" daje wynik: %s' % (s, czyTylkoMaleLiteryBezDiakrytycznych(s)))
    s = 'ą'
    print('"%s" daje wynik: %s' % (s, czyTylkoMaleLiteryBezDiakrytycznych(s)))
    s = 'ę'
    print('"%s" daje wynik: %s' % (s, czyTylkoMaleLiteryBezDiakrytycznych(s)))
    s = 'ĄĘć'
    print('"%s" daje wynik: %s' % (s, czyTylkoMaleLiteryBezDiakrytycznych(s)))

def testCzyDataWFormacieYYYY_MM_DD() :
    s = '2018-05-0'
    print('"%s" daje wynik: %s' % (s, czyDataWFormacieYYYY_MM_DD(s)))
    s = '2018-05-32'
    print('"%s" daje wynik: %s' % (s, czyDataWFormacieYYYY_MM_DD(s)))
    s = '2018-05-a'
    print('"%s" daje wynik: %s' % (s, czyDataWFormacieYYYY_MM_DD(s)))
    s = '2018-05-31a'
    print('"%s" daje wynik: %s' % (s, czyDataWFormacieYYYY_MM_DD(s)))
    s = '2018-05-31 '
    print('"%s" daje wynik: %s' % (s, czyDataWFormacieYYYY_MM_DD(s)))
    s = 'a2018-05-31'
    print('"%s" daje wynik: %s' % (s, czyDataWFormacieYYYY_MM_DD(s)))
    s = ' 2018-05-31'
    print('"%s" daje wynik: %s' % (s, czyDataWFormacieYYYY_MM_DD(s)))
    s = '123-05-31'
    print('"%s" daje wynik: %s' % (s, czyDataWFormacieYYYY_MM_DD(s)))
    s = '2018-13-12'
    print('"%s" daje wynik: %s' % (s, czyDataWFormacieYYYY_MM_DD(s)))
    s = '9999-12-31'
    print('"%s" daje wynik: %s' % (s, czyDataWFormacieYYYY_MM_DD(s)))
    s = '0000-01-01'
    print('"%s" daje wynik: %s' % (s, czyDataWFormacieYYYY_MM_DD(s)))
    s = '2018 -05-31'
    print('"%s" daje wynik: %s' % (s, czyDataWFormacieYYYY_MM_DD(s)))
    s = '2018-05- 31'
    print('"%s" daje wynik: %s' % (s, czyDataWFormacieYYYY_MM_DD(s)))

# testCzyTylkoMaleLitery()
# testCzyDataWFormacieYYYY_MM_DD()

# print(czyDataWFormacieYYYY_MM_DD("2018-05-1"))