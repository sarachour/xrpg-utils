import src.rolls as rolls
import src.character as charlib
import src.traits as traitlib
import src.gear as gearlib
import z3 
import numpy.random as random

class AnySkillBetween:

    def __init__(self,count,min_val,max_val):
        self.min_val = min_val
        self.max_val = max_val
        self.count = count

    @classmethod
    def load(cls,args):
        min_val = args["min"] if "min" in args else 0
        max_val = args["max"] if "max" in args else 9999
        count = args["count"] if "count" in args else 1
        return AnySkillBetween(count,min_val,max_val)


    def apply(self,chgen):
        expr = []
        for skill in charlib.Skill:
            clause = z3.And(chgen.skills[skill] >= self.min_val, chgen.skills[skill] <= self.max_val)
            expr.append(z3.If(clause,1,0))
        chgen.user_cstr(sum(expr) >= self.count)

class AnyRollBetween:

    def __init__(self,count,min_val,max_val,priority=rolls.Priority.Any):
        self.min_val = min_val
        self.max_val = max_val
        self.count = count
        self.priority = priority

    @classmethod
    def load(cls,args):
        min_val = args["min"] if "min" in args else 0
        max_val = args["max"] if "max" in args else 9999
        count = args["count"] if "count" in args else 1
        priority = args["priority"] if "priority" in args else rolls.Priority.Any
        return AnyRollBetween(count,min_val,max_val, priority=priority)

    def apply(self,chgen):
        expr = []
        for intel,skill in rolls.get_rolls(priority=self.priority):
            term = chgen.skills[skill] + chgen.ints[intel]
            clause = z3.And(term >= self.min_val, term <= self.max_val)
            expr.append(z3.If(clause,1,0))
        chgen.user_cstr(sum(expr) >= self.count)


class RandomIntelligence:

    def __init__(self,count=1,min_val=0,max_val=999):
        self.count = count
        self.min_val = min_val
        self.max_val = max_val
        pass

    @classmethod
    def load(cls,args):
        count = args["count"] if "count" in args else 1
        min_val = args["min"] if "min" in args else 0
        max_val = args["max"] if "max" in args else 999
        return RandomIntelligence(count,min_val,max_val)

    def apply(self,chgen):
        for _ in range(self.count):
            intel = random.choice(list(charlib.Intelligences))
            cstr = z3.And(chgen.ints[intel] <= self.max_val, chgen.ints[intel] >= self.min_val) 
            chgen.user_cstr(cstr)


class RandomTrait:

    def __init__(self,slot,trait_list=[],options=1):
        self.slot = slot
        self.trait_list =trait_list
        self.options = options
        pass

    @classmethod
    def load(cls,args):
        slot = charlib.Traits(args["slot"])
        if isinstance(args["list"],list):
            listels = list(map(lambda el: traitlib.TraitList(el), args["list"]))
        else:
           listels =  [traitlib.TraitList(args["list"])]
        options = args["options"] if "options" in args else -1
        return RandomTrait(slot,trait_list=listels,options=options)

    def apply(self,chgen):
        slot_var = chgen.traits[self.slot]

        trait_options = []
        for tr in self.trait_list:
            trait_options += list(traitlib.get_trait_list(tr))

        if self.options > 0:
            opts = random.choice(trait_options,self.options)
        else:
            opts = trait_options

        expr = []
        for trait in opts:
            expr.append(slot_var == traitlib.get_index(trait))

        chgen.user_cstr(z3.Or(*expr))


class RandomGear:

    def __init__(self,slot,gear_list=[],options=1):
        self.slot = slot
        self.gear_list = gear_list 
        self.options = options
        pass

    @classmethod
    def load(cls,args):
        slot = charlib.Gear(args["slot"])
        if isinstance(args["list"],list):
            listels = list(map(lambda el: gearlib.GearList(el), args["list"]))
        else:
           listels =  [gearlib.GearList(args["list"])]
        options = args["options"] if "options" in args else -1
        return RandomGear(slot,gear_list=listels,options=options)

    def apply(self,chgen):
        slot_var = chgen.gear[self.slot]

        gear_options = []
        for tr in self.gear_list:
            gear_options += list(gearlib.get_gear_list(tr).keys())


        if self.options > 0:
            opts = random.choice(gear_options,self.options)
        else:
            opts = gear_options

        expr = []
        for gear in opts:
            expr.append(slot_var == gearlib.get_index(gear))

        chgen.user_cstr(z3.Or(*expr))
