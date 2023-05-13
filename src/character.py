from enum import Enum
import numpy as np
import numpy.random as random

class Traits(Enum):
    Trait1 = "trait1"
    Trait2 = "trait2"
    Trait3 = "trait3"

class Gear(Enum):
    Gear1 = "gear1"
    Gear2 = "gear2"
    Gear3 = "gear3"
    Gear4 = "gear4"
    Gear5 = "gear5"

class OtherStats(Enum):
    Move = "move"
    Run = "run"
    Strength = "strength"
    Toughness = "toughness"
    Torso = "torso"


class Intelligences(Enum):
    Logical = "logical"
    Spatial = "spatial"
    Linguistic = "linguistic"
    Kinesthetic = "kinesthetic"
    Musical = "musical"
    Interpersonal = "interpersonal"
    Intrapersonal = "intrapersonal"


class IntelligenceStats:

    def __init__(self):
        self.stats = dict(map(lambda it: (it,0), Intelligences))


    def __repr__(self):
        stmts = []
        def add(s):
            stmts.append(s)

        for it,val in self.stats.items():
            add("%s = %d" % (it.value, val))
        return "\n".join(stmts)


class Skill(Enum):
    Deception = "deception"
    Empathy = "empathy"
    Persuasion = "persuasion"

    Academics = "academics"
    Artistry = "artistry"
    Mysteries = "mysteries"

    BattleSpeed = "battle speed"
    Brawling = "brawling"
    Guns = "guns"

    Agility = "agility"
    Endurance = "endurance"
    MuscleTraining = "muscle training"

    Hardware = "hardware"
    Pilot = "pilot"
    Software = "software"

    Intimidation = "intimidation"
    Grit = "grit"
    Psyche = "psyche"

    Drive = "drive"
    Perception = "perception"
    Stealth = "stealth"


class SkillClass(Enum):
    Charisma = "charisma"
    Education = "education"
    Fight = "fight"
    Physique = "physique"
    Technology = "technology"
    Willpower = "willpower"
    Wits = "wits"

    def abbrevs(self):
        raise NotImplementedError

    @classmethod
    def get_class(clsT,sk):
        for skcls in clsT:
            if sk in skcls.skills():
                return skcls

    def skills(self):
        if self == SkillClass.Charisma:
            yield Skill.Deception
            yield Skill.Empathy
            yield Skill.Persuasion
        elif self == SkillClass.Education:
            yield Skill.Academics
            yield Skill.Artistry
            yield Skill.Mysteries
        elif self == SkillClass.Fight:
            yield Skill.BattleSpeed
            yield Skill.Brawling
            yield Skill.Guns
        elif self == SkillClass.Physique:
            yield Skill.Agility
            yield Skill.Endurance
            yield Skill.MuscleTraining
        elif self == SkillClass.Technology:
            yield Skill.Hardware
            yield Skill.Pilot
            yield Skill.Software
        elif self == SkillClass.Willpower:
            yield Skill.Grit
            yield Skill.Intimidation
            yield Skill.Psyche
        elif self == SkillClass.Wits:
            yield Skill.Drive
            yield Skill.Perception
            yield Skill.Stealth
        else:
            raise NotImplementedError

class SkillStats:
        
    def __init__(self):
        self.aptitudes = {}
        self.stats = {}
        for cls in SkillClass:
            self.aptitudes[cls] = 0
            self.stats[cls] = dict(map(lambda sk : (sk,0), cls.skills()))

    def get_skill(self,sk):
        for skcls,skls in self.stats.items():
            for csk,val in skls.items():
                if csk == sk:
                    return val
        raise Exception("undefined skill") 



    def __repr__(self):
        stmt = []
        def add(s):
            stmt.append(s)
        for skcls,skls in self.stats.items():
            add("%s [%d]" % (skcls.value,self.aptitudes[skcls]))
            for skl,score in skls.items():
                add("  %s = %d" % (skl.value,score))
        return "\n".join(stmt)

        
class Character:

    def __init__(self,name):
        self.name = name
        self.skills = SkillStats()
        self.intelligences = IntelligenceStats()
        self.other = {}
        self.traits = {}
        self.gear = {}
        for trait in Traits:
            self.traits[trait] = ""
        
        for gear in Gear:
            self.gear[gear] = ""


    def finalize(self):
        self.other[OtherStats.Move] = self.skills.get_skill(Skill.Agility) + 1
        self.other[OtherStats.Run] = self.skills.get_skill(Skill.Agility) + 8
        self.other[OtherStats.Strength] = self.skills.get_skill(Skill.MuscleTraining) + 1
        self.other[OtherStats.Toughness] = self.skills.get_skill(Skill.Endurance) + 1

        self.other[OtherStats.Torso] = self.skills.get_skill(Skill.Endurance) + 20 + 2

    def __repr__(self):
        st = ""
        st += str(self.intelligences)
        st += "\n\n"
        st += str(self.skills)
        return st





