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

    def abbrev(self):
        if Intelligences.Logical == self:
            return "logic"
        if Intelligences.Spatial == self:
            return "spatl"
        if Intelligences.Linguistic == self:
            return "ling"
        if Intelligences.Kinesthetic == self:
            return "kinth"
        if Intelligences.Musical == self:
            return "music"
        if Intelligences.Interpersonal == self:
            return "inter"
        if Intelligences.Intrapersonal == self:
            return "intra"

class IntelligenceStats:

    class Info:

        def __init__(self,base,exp,experience):
            self.base_points = base
            self.exp_points = exp
            self.experience_cost = experience

        @property
        def value(self):
            return self.base_points + self.exp_points

    def __init__(self):
        self.stats = {}
        for intel in Intelligences:
            self.stats[intel] = IntelligenceStats.Info(0,0,0)



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

    def abbrev(self):
        if self == Skill.Deception:
            return "decpt"
        elif self == Skill.Empathy:
            return "empth"
        elif self == Skill.Persuasion:
            return "persu"
        elif self == Skill.Academics:
            return "acadm"
        elif self == Skill.Artistry:
            return "arts "
        elif self == Skill.Mysteries:
            return "mystr"
        elif self == Skill.BattleSpeed:
            return "bspd "
        elif self == Skill.Brawling:
            return "brawl"
        elif self == Skill.Guns:
            return "guns "
        elif self == Skill.Agility:
            return "agilt"
        elif self == Skill.Endurance:
            return "endur"
        elif self == Skill.MuscleTraining:
            return "muscl"
        elif self == Skill.Hardware:
            return "hardw"
        elif self == Skill.Pilot:
            return "pilot"
        elif self == Skill.Software:
            return "softw"
        elif self == Skill.Intimidation:
            return "intim"
        elif self == Skill.Grit:
            return "grit "
        elif self == Skill.Psyche:
            return "psych"
        elif self == Skill.Drive:
            return "drive"
        elif self == Skill.Perception:
            return "percp"
        elif self == Skill.Stealth:
            return "stlth"

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

    def abbrev(self):
        if self == SkillClass.Charisma:
            return "CHAR"
        elif self == SkillClass.Education:
            return "EDUC"
        elif self == SkillClass.Fight:
            return "FGHT"
        elif self == SkillClass.Physique:
            return "PHYS"
        elif self == SkillClass.Technology:
            return "TECH"
        elif self == SkillClass.Willpower:
            return "WILL"
        elif self == SkillClass.Wits:
            return "WITS"
            
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

    class Info:

        def __init__(self,base,free,exp,experience_cost):
            self.base_points = base
            self.free_points = free
            self.exp_points = exp
            self.experience_cost = experience_cost

        @property
        def value(self):
            return self.base_points + self.free_points + self.exp_points



    def __init__(self):
        self.aptitudes = {}
        self.stats = {}


        for cls in SkillClass:
            self.aptitudes[cls] = 0
            for sk in cls.skills():
                self.stats[sk] = SkillStats.Info(0,0,0,0)


    def get_skill(self,sk):
        return self.stats[sk]


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
        self.experience = 0
        self.novice = False
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
        self.other[OtherStats.Move] = self.skills.get_skill(Skill.Agility).value + 1
        self.other[OtherStats.Run] = self.skills.get_skill(Skill.Agility).value + 8
        self.other[OtherStats.Strength] = self.skills.get_skill(Skill.MuscleTraining).value + 1
        self.other[OtherStats.Toughness] = self.skills.get_skill(Skill.Endurance).value + 1

        self.other[OtherStats.Torso] = self.skills.get_skill(Skill.Endurance).value + 20 + 2

    def __repr__(self):
        st = ""
        st += str(self.intelligences)
        st += "\n\n"
        st += str(self.skills)
        return st





