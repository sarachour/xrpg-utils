

def get_intelligence_implications():
    yield IntelligenceBetween(Intelligences.Kinesthetic,1,3), SkillBetween(Skill.MuscleTraining, 1,3)

# link intelligences to background traints
def get_background_implications():
    yield "Amputee", IntelligenceBetween(Intelligences.Kinesthetic,1,3)
    yield "Perfect Hearing", IntelligenceBetween(Intelligences.Musical,5,9)
    yield "Blind", IntelligenceBetween(Intelligences.Spatial,1,2)
    yield "Deaf", IntelligenceBetween(Intelligences.Musical,1,2)
    yield "Sharp Eyes", IntelligenceBetween(Intelligences.Musical,5,9)
    yield "High IQ", IntelligenceBetween(Intelligences.Logical,5,9)
    yield "Socially Disastrous", IntelligenceBetween(Intelligences.Interpersonal,1,2)

def sane_character_constraints():
    for bg, cstr in get_background_implications():
        yield ImpliesConstraint(SelectTraits([bg]),cstr)

    for intel,cstr in get_intelligence_implications():
        yield ImpliesConstraint(intel,cstr)
