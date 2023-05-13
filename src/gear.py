from enum import Enum

class GearList(Enum):
    Weapons = "weapons"
    Tech = "tech"

def _ordered_traits(els):
    ord_els = list(els)
    ord_els.sort()
    return ord_els

def get_electronics():
    yield "Smart Phone",700.00
    yield "Tablet computer",400.0
    yield "Laptop", 1000

def get_weapons():
    yield "Knife",50
    yield "Taser",500

def get_gear_list(lst):
    if GearList.Tech:
        return dict(list(get_electronics()))
    elif GearList.Knife:
        return dict(list(get_weapons()))
    else:
        return []



def get_price(el):
    for gear in GearList:
        geardict = get_gear_list(gear)
        if el in geardict:
            return geardict[el]
    raise Exception("no price: <%s>" % el)

def get_all_gear():
    c = []
    for gear in GearList:
        c += list(get_gear_list(gear).keys())

    return _ordered_traits(c)

def get_gear(idx):
    return get_all_gear()[idx]

def get_index(gear):
    c = get_all_gear()
    return c.index(gear)