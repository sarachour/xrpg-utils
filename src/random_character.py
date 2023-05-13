from lib.character import *

def dice_roll(num_sides):
    return random.randint(1,num_sides+1) 

def random_intelligence_proficient():
    return max(dice_roll(6),dice_roll(6))

def random_intelligence_normal():
    return max(dice_roll(4),dice_roll(4))
      

def random_character(name, experience=0):
    char = Character(name)

    # select three proficient intelligences
    prof_ints = random.choice(list(Intelligences), 3)
    normal_ints = list(filter(lambda it: not it in prof_ints, 
                            list(Intelligences)))
    for it in prof_ints:
        char.intelligences.stats[it] = 1+random_intelligence_proficient()

    for it in normal_ints:
        char.intelligences.stats[it] = 1+random_intelligence_normal()

    scores = [1,2,3,4,5,6,7]
    random.shuffle(scores)
    for score, skcls in zip(scores,list(SkillClass)):
        char.skills.aptitudes[skcls] = score
        alloc = random_allocate_skills(score, list(skcls.skills()))
        for skill,value in alloc.items():
            char.skills.stats[skcls][skill] = value

    return char    
    
def random_allocate_skills(points,skills):
    def highest_skills(allocs):
        val = np.max(list(allocs.values()))
        return list(map(lambda t: t[0], 
            filter(lambda t: t[1] == val, allocs.items())))

    allocs = dict(map(lambda s: (s,0), skills))
    while points > 0:
        skill = random.choice(skills)
        highest = highest_skills(allocs)
        if skill in highest and points >= 2:
            points -= 2
            allocs[skill] += 1
        else:
            allocs[skill] += 1
            points -= 1


    return allocs

