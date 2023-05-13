import random
import src.traits as traitlib
from src.character import Skill, Intelligences
import z3

class CharacterCstr:

    def __init__(self):
        pass

    def apply(self,chgen):
        raise NotImplementedError

class SelectTraits:

    def __init__(self,traits):
        self.traits = traits 

    def apply(self,cstrprob):
        exprs = False
        for var in [cstrprob.background,cstrprob.mental,cstrprob.physical]:
            for tr in self.traits:
                exprs = z3.Or(traitlib.get_index(tr) == var,exprs)

        yield exprs

class IntelligenceBetween:

    def __init__(self,integ,min_val,max_val):
        self.min_val = min_val
        self.max_val = max_val
        self.integ = integ

    def apply(self,chgen):
        yield z3.And(chgen.ints[self.integ] >= self.min_val, chgen.ints[self.integ] <= self.max_val)
    
class SkillBetween:

    def __init__(self,skill,min_val,max_val):
        self.min_val = min_val
        self.max_val = max_val
        self.skill = skill

    def apply(self,chgen):
        yield z3.And(chgen.skills[self.skill] >= self.min_val, chgen.skills[self.skill] <= self.max_val)
    
        
class AptitudeAtLeast:

    def __init__(self,apt,val):
        self.val = val
        self.apt = apt
    
    def apply(self,chgen):
        yield chgen.skill_classes[self.apt] >= apt

class RollAtLeast:

    def __init__(self,intg,skill,val):
        self.val = val
        self.intg = intg
        self.skill = skill
    
    def apply(self,chgen):
        yield chgen.skills[self.skill] + chgen.ints[self.intg] >= self.val

class AnySkillAtLeast:

    def __init__(self,count,val):
        self.val = val
        self.count = count

    def apply(self,chgen):
        expr = []
        for skill in Skill:
            expr.append(z3.If(chgen.skills[skill] >= self.val,1,0))
        yield sum(expr) >= self.count

class AnySkillAtLeast:

    def __init__(self,count,val):
        self.val = val
        self.count = count

    def apply(self,chgen):
        expr = []
        for skill in Skill:
            expr.append(z3.If(chgen.skills[skill] >= self.val,1,0))
        yield sum(expr) >= self.count

class AnyRollBetween:

    def __init__(self):
        pass
class ImpliesConstraint:

    def __init__(self,cstr1,cstr2):
        self.cstr1 = cstr1
        self.cstr2 = cstr2

    def apply(self,chgen):
        els = list(self.cstr1.apply(chgen))
        assert(len(els) == 1)
        for c2 in self.cstr2.apply(chgen):
            yield z3.Implies(els[0], c2)




    
