from gen import charlang

def random_character_constraints(num_backgrounds=2, num_expert=2, num_normal=4, num_good_rolls=5,num_great_rolls=2):
    options = random.choices(traitlib.get_backgrounds(),k=2) + \
        random.choices(traitlib.get_physical(),k=2) + \
        random.choices(traitlib.get_mental(),k=2)

    yield SelectTraits(options)

    expert = 5
    normal = 3

    yield AnySkillAtLeast(count=num_expert,val=expert)
    yield AnySkillBetween(count=normal,min_val=normal,max_val=expert)

    options = random.choices(list(get_rolls()), k=num_good_rolls)
    good_roll = 6
    for intel,skill in options:
        yield RollAtLeast(intel,skill,good_roll)

    options = random.choices(list(get_rolls()), k=num_good_rolls)
    great_roll = 8
    for intel,skill in options:
        yield RollAtLeast(intel,skill,great_roll)


ELEMENT_DICT = {
    "any-skills-between": charlang.AnySkillBetween,
    "any-rolls-between": charlang.AnyRollBetween,
    "random-trait": charlang.RandomTrait,
    "random-gear": charlang.RandomGear,
    "random-intelligence-between": charlang.RandomIntelligence

}

def load(text):
    def cast_term(x):
        try:
            return int(x)
        except ValueError:
            return x


    def make_dict_el(term):
        key,value = term.split("=")
        if "," in value:
            value = list(map(lambda x: cast_term(x), value.split(",")))
        else:
            value = cast_term(value)

        return (key,value)

    for line in text.split("\n"):
        if line.startswith("#"):
            continue
        if line.strip() == "":
            continue
        
        terms = line.split(" ")
        keyw = terms[0]
        args = dict(map(lambda term: make_dict_el(term), terms[1:]))

        if keyw in ELEMENT_DICT:
            cstr = ELEMENT_DICT[keyw].load(args)
            yield cstr
        else:
            print("[WARN] unsupported: %s" % line)
            