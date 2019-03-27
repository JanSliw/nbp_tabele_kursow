

def dokumentZeSciezki(sciezka):
    import xml.dom.minidom as __minidom
    drzewo = __minidom.parse(file=sciezka)
    return drzewo.documentElement


def pobierzAtrybutZElementu(atrybut, element):
    wyn = ''
    if element.hasAttribute(atrybut):
        wyn = element.getAttribute(atrybut)
    return wyn


def wybierzDzieciZElementuPoTagu(element, tag):
    return element.getElementsByTagName(tag)


def zwrocDaneZElementu(element):
    return element.childNodes[0].data


def pokazPierwszeDzieckoZElementuPoTagu(element, tag):
    return wybierzDzieciZElementuPoTagu(element=element, tag=tag)[0]


def zbierzDaneZPierwszegoDzieckaZElementuPoTagu(element, tag):
    pierwszeDziecko = pokazPierwszeDzieckoZElementuPoTagu(element, tag)
    return zwrocDaneZElementu(pierwszeDziecko)