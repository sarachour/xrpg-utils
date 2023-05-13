import src.traits as traitlib
import src.gear as gearlib
from src.character import SkillClass, Skill, Intelligences

base_square = "\u25A3"
exp_square = "\u25C8"
white_square = "\u25A2"
free_square = "\u25CF"

preamble = '''
==== LEGEND ===
[exp=#]: the amount of experience points spent on skill or intelligence.
{base_square}: basic intelligence/skill point allocation.
{free_square}: skill point allocation done with 10 free points.
{exp_square}: intelligence/skill point allocations achieved with experience points.
{white_square}: unallocated
===============
'''.format(base_square=base_square, exp_square=exp_square, \
            free_square=free_square,white_square=white_square)

def build_intelligence_bubble_info(info):
  
    bubbles = []
    total = 8
    for idx in range(info.base_points):
        bubbles.append(base_square)
    for idx in range(info.exp_points):
        bubbles.append(exp_square) 
    for idx in range(total - info.value):
        bubbles.append(white_square)

    text = "".join(bubbles[0:2])
    text += " "
    text += "".join(bubbles[2:5])
    text += " "
    text += "".join(bubbles[5:])
    return text 

def build_skill_bubble_info(info):
    bubbles = []
    total = 8
    for idx in range(info.base_points):
        bubbles.append(base_square)
    for idx in range(info.free_points):
        bubbles.append(free_square) 
    for idx in range(info.exp_points):
        bubbles.append(exp_square) 
    for idx in range(total - info.value):
        bubbles.append(white_square)

    text = "".join(bubbles[0:4])
    text += " "
    text += "".join(bubbles[4:8])
    return text 


def generate_character_summary(char):
    yield preamble
    yield "name: %s" % char.name
    yield ""
    total_cost = 0
    for idx,(trait,name) in enumerate(char.traits.items()):
        exp_cost = traitlib.get_cost(name)
        yield "%d] %s [exp=%d]" % (idx, name, exp_cost)
        total_cost += exp_cost
    yield ""
    yield "-------------------------------"
    yield "is a novice? %s" % ("yes" if char.novice else "no")
    yield "total experience: %d - (%d)  = %d" % (char.experience, total_cost, -total_cost+char.experience)
    yield "-------------------------------"
    total_experience = sum(map(lambda intg: intg.experience_cost, char.intelligences.stats.values()))
    yield "=== INTELLIGENCES [exp=%d] ===" % total_experience
    for intel,info in char.intelligences.stats.items():
        text = build_intelligence_bubble_info(info)
        if info.experience_cost > 0:
            yield "%s\t\t %s \t\t[exp=%d]" % (intel.abbrev(), text,info.experience_cost)
        else:
            yield "%s\t\t %s" % (intel.abbrev(),text)
    
    total_experience = sum(map(lambda sk: char.skills.stats[sk].experience_cost, Skill))
    yield "======== SKILLS [exp=%d] =========" % total_experience
    for skcls in SkillClass:
        skills = list(skcls.skills())
        total_experience = sum(map(lambda sk: char.skills.stats[sk].experience_cost, skills))
        rank = char.skills.aptitudes[skcls]
        yield "------ [%d] %s -----" % (rank,skcls.abbrev())

        for sk in skills:
            info = char.skills.stats[sk]
            text = build_skill_bubble_info(info)
            if info.experience_cost > 0:
                yield "%s\t\t%s \t\t[exp=%d]" % (sk.abbrev(), text, info.experience_cost)
            else:
                yield "%s\t\t%s" % (sk.abbrev(), text)

def write_character_log(file,char):
    with open(file,"w") as fh:
        for line in generate_character_summary(char):
            fh.write(line+"\n")
    