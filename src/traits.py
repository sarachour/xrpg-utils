from enum import Enum

class TraitList(Enum):
    Background = "backgrounds"
    Physical = "physical"
    Mental = "mental"
    Social = "social"

backgrounds = {
    "Doctor": 4,
    "Private Investigator": 3,
    "Street Rat": -3,
    "Cop": 4,
    "Detective": 6,
    "Spy": 8,
    "Burned Spy": 2,
    "Preacher": 6,
    "Celebrity": 7,
    "Active Military": 2,
    "Veteran": 2,
    "Illegal Immigrant": -3,
    "Socially Disastrous": -3,
    "Greed": -2,
    "Addicted to Love": -2,
    "Addiction": -2,
    "Gung Ho": -1,
    "Pig-Headed": -2,
    "Nasty Piece of Work": -5,
    "Perennially Cheerful": 3,
    "Annoyingly Cheerful": -1,
    "Depression": -2,
    "Psychological Problems": -3,
    "Cool Head": 2,
    "Vengeance": -2,
    "True Faith": 3,
    "Loyalty": 2,
    "Hardened": 4
}

physical = {
    "Petite": -2,
    "Big and Tall": 3,
    "Limbs like Tree Trunks": 7,
    "Wiry Strength": 2,
    "Tough as Old Leather": 2,
    "Soft Belly": -2,
    "Extra Fluffy": -5,
    "Sharp Eyes": 2,
    "Perfect Hearing": 2,
    "Keen Scent and Taste": 2,
    "Sensual": 1,
    "Young": -2,
    "Old": -3,
    "Blind": -6,
    "Deaf": -6,
    "Deformed": -2.5,
    "Beaten with the Ugly Stick": -1,
    "Attractive": 2,
    "Beautiful/Dashing": 5,
    "Scarred": -1,
    "Amputee": -5,
    "Irish Liver": 1,
    "Perfect Pitch": 2
}

# mental and social
mental = {
    "Touch of Genius": 3,
    "High IQ": 4,
    "Sense of Duty": 2,
    "Well-Travelled": 1,
    "Socially Oblivious": -1,
    "Conceal Carry Permit": 1,
    "Professional License": 1,
    "Vehicle License": 1,
    "Friends in High Places": 2,
    "Friends in Low Places": 2,
    "Moneyed Individual": 3,
    "Destitute": -2,
    "Friendless": -3,
    "Hunted": -3,
    "Foreigner": -1,
    "Military Training": 2,
    "Backing": 3,
    "Interns": 2,
    "Highly Trained": 3,
    "Inexperienced": 7,
    "Experienced": -7,
    "Access": 2,
    "Fame": 2,
    "Loyal Pet": 2,
    "Loyal Friend": 3,
    "Beautiful Girlfriend": -3,
    "In Debt": -2,
    "Duty": -1,
    "Burned": -3,
    "Sentenced": -3,
    "Legal Immunity": 2
}

ALL_TRAITS = dict(list(mental.items()) + list(physical.items()) + list(backgrounds.items()))

def _ordered_traits(els):
    ord_els = list(els)
    ord_els.sort()
    return ord_els


def get_trait_list(lst):
    if TraitList.Background:
        return _ordered_traits(backgrounds.keys())
    elif TraitList.Physical:
        return _ordered_traits(physical.keys())
    elif TraitList.Mental:
        return _ordered_traits(mental.keys())
    else:
        raise NotImplementedError

def get_traits():
    lst = []
    for el in TraitList:
        lst += get_trait_list(el)

    return _ordered_traits(lst)

def get_trait(idx):
    return get_traits()[idx]

def get_cost(trait):
    return ALL_TRAITS[trait]

def get_index(trait):
    trs = get_traits()
    return trs.index(trait)
