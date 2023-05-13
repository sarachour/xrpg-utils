from src.character import *
import src.traits as traitlib
import src.gear as gearlib
import src.proficiencies as proflib
import z3
import random
import names


def exactly_one(vars,val):
    return (1 == sum(map(lambda v: z3.If(v == val, 1, 0), vars)))

def z3_max(variable_iter):
    expr = -1
    variables = list(variable_iter)
    for v in variables:
        ites = list(map(lambda v2: v >= v2, variables))
        clause = z3.And(*ites)
        expr = z3.If(clause,v,expr) 

    return expr

class Z3CharGen:

    def __init__(self):
        self.ints = {}
        self.ints_pb = {}
        self.ints_exp = {}

        # costs
        self.costs_exp = {}
        self.costs_money = {}

        self.traits = {}
        self.gear = {}

        self.int_points = z3.Int("INT_POINTS")
        self.skill_points = z3.Int("SKILL_POINTS")
        self.experience  = z3.Int("EXPERIENCE")
        self.money = z3.Int("MONEY")
        self.cstrs = []
        self.user_cstrs = []

        self.initialize()

    def initialize(self,experienced=True):
        # inexperienced characters cannot raise skills past 4
        self.experienced = experienced
        self.initialize_intelligences()
        self.initialize_skills()
        self.initialize_traits()
        self.initialize_gear()
        self.initialize_licenses_and_proficiencies()
        self.finalize()

    def initialize_licenses_and_proficiencies(self):
        pass

    def initialize_gear(self):
        num_gear = len(gearlib.get_all_gear())

        for gear in Gear:
            self.gear[gear]  = z3.Int(gear.value)
            self.costs_money[gear] = z3.Int(gear.value+":COST")
            self.cstr(z3.And(self.gear[gear] >= 0, self.gear[gear] < num_gear))

        for slot in Gear:
            expr = 9999999
            for gear in gearlib.get_all_gear():
                cost = gearlib.get_price(gear)
                expr = z3.If(gearlib.get_index(gear) == self.gear[slot], cost, expr)

            self.cstr(self.costs_money[slot] == expr)

        for slot1 in Gear:
            for slot2 in Gear:
                if slot1 == slot2:
                    continue

                self.cstr(self.gear[slot1] != self.gear[slot2])


    def initialize_traits(self):
        num_traits = len(traitlib.get_traits())

        for trait in Traits:
            self.traits[trait]  = z3.Int(trait.value)
            self.costs_exp[trait] = z3.Int(trait.value+":COST")
            self.cstr(z3.And(self.traits[trait] >= 0, self.traits[trait] < num_traits))

        for slot in Traits:
            expr = 9999999
            for trait in traitlib.get_traits():
                cost = traitlib.get_cost(trait)
                expr = z3.If(traitlib.get_index(trait) == self.traits[slot], cost, expr)

            self.cstr(self.costs_exp[slot] == expr)

        for slot1 in Traits:
            for slot2 in Traits:
                if slot1 == slot2:
                    continue
                
                self.cstr(self.traits[slot1] != self.traits[slot2])


    def initialize_intelligences(self):

        for intg in Intelligences:
            self.ints[intg] = z3.Int(intg.value)
            self.cstr(z3.And(self.ints[intg] >= 1, self.ints[intg] <= 8))

            pb = self.ints_pb[intg] = z3.Int(intg.value+":PB")
            self.cstr(z3.And(self.ints_pb[intg] >= 0, self.ints_pb[intg] <= 4))

            #points bought with experience
            exp = self.ints_exp[intg] = z3.Int(intg.value+":EXP")
            self.cstr(z3.And(self.ints_exp[intg] >= 0, self.ints_exp[intg] <= 7))
            self.cstr(z3.And(self.ints[intg] == pb+exp+2))


            # each additional point costs as much as the point value
            cost = self.costs_exp[intg] = z3.Int("COST:"+intg.value+":EXP")
            self.cstr(cost == self.intelligence_cost(intg))



        # cannot exceed number of points
        self.cstr(sum(self.ints_pb.values()) == self.int_points)

        
    def initialize_skills(self):
        
        self.skills = {}
        self.skills_pb = {}
        self.skills_free = {}
        self.skills_exp = {}
        for sk in Skill:
            self.skills[sk] = z3.Int(sk.value)
            self.cstr(z3.And(self.skills[sk] >= 0, self.skills[sk] <= 8))


            pb = self.skills_pb[sk] = z3.Int(sk.value+":PB")
            self.cstr(z3.And(self.skills_pb[sk] >= 0, self.skills_pb[sk] <= 4))

            free = self.skills_free[sk] = z3.Int(sk.value+":FREE")
            self.cstr(z3.And(self.skills_free[sk] >= 0, self.skills_free[sk] + self.skills_pb[sk] <= 4))

            exp = self.skills_exp[sk] = z3.Int(sk.value+":EXP")
            self.cstr(z3.And(self.skills_exp[sk] >= 0, self.skills_exp[sk] <= 8))

            self.cstr(z3.And(self.skills[sk] == pb+exp+free))

        # compute costs for kills
        for sk in Skill:
            cost = self.costs_exp[sk] = z3.Int("COST:"+sk.value+":EXP")
            self.cstr(cost == self.skill_cost(sk))

        self.skill_classes = {}
        for sk in SkillClass:
            self.skill_classes[sk] = z3.Int(sk.value)
            self.cstr(z3.And(self.skill_classes[sk] >= 1,self.skill_classes[sk] <= 7))
            self.cstr(self.skill_classes[sk]==sum(map(lambda skill: self.skills_pb[skill], sk.skills())))

        self.cstr(sum(self.skills_free.values()) == self.skill_points)

        for i in range(1,8):
            self.cstr(exactly_one(self.skill_classes.values(), i))

    def finalize(self):
        # cannot spend more than alloted experience
        self.cstr(self.experience == sum(self.costs_exp.values()))

        self.move = z3.Int(OtherStats.Move.value)
        self.toughness = z3.Int(OtherStats.Toughness.value)
        self.run = z3.Int(OtherStats.Run.value)
        self.strength = z3.Int(OtherStats.Strength.value)

        self.cstr(self.move == self.skills[Skill.Agility] + 1)
        self.cstr(self.run == self.skills[Skill.Agility] + 8)
        self.cstr(self.toughness == self.skills[Skill.Agility] + 1)
        self.cstr(self.strength == self.skills[Skill.MuscleTraining] + 1)

    def intelligence_cost(self,intg):
        exprs = []
        for ptvals in range(1,8):
            exp = z3.If(self.ints_exp[intg] >= ptvals, self.ints[intg]-(ptvals-1), 0)
            exprs.append(exp)
        return sum(exprs)

    def skill_cost(self,skill):
        # If this skill will be the highest in its domain, after this purchase, the dot costs 2 xp instead of 1.
        # If raising a skill past 5, the cost goes up by 1 for each additional dot. (So your 6th dot costs 2xp, the 7th costs 3xp, and so on.)
        skillcls = SkillClass.get_class(skill)
        other_skills = list(skillcls.skills())
        highest_skill = z3_max(map(lambda sk: self.skills[sk], other_skills))
        is_skill_highest = (highest_skill == self.skills[skill])

        costfn = self.skills_exp[skill]
        costfn += z3.If(is_skill_highest, self.skills_exp[skill], 0)
        costfn += z3.If(self.skills[skill] >= 6, 1,0)
        costfn += z3.If(self.skills[skill] >= 7, 2,0)
        costfn += z3.If(self.skills[skill] >= 8, 3,0)
        
        return costfn

    def add_skill_sanity_constraints(self):
        for skillcls in SkillClass:
            intgs = list(skillcls.intelligences())
            skills = list(skillcls.skills())


    def cstr(self,c):
        self.cstrs.append(c)

    def user_cstr(self,c):
        self.user_cstrs.append(c)

        

def model_to_character(name,chgen,model):
    ch = Character(name)
    ch.experience = model[chgen.experience].as_long()
    for intg in Intelligences:
        val = model[chgen.ints[intg]]
        val_pb = model[chgen.ints_pb[intg]].as_long()
        val_exp = model[chgen.ints_exp[intg]].as_long()
        val_cost = model[chgen.costs_exp[intg]].as_long()

        ch.intelligences.stats[intg].base_points = val_pb+2
        ch.intelligences.stats[intg].exp_points = val_exp
        ch.intelligences.stats[intg].experience_cost = val_cost
        assert(ch.intelligences.stats[intg].value == val.as_long())

    for skcls in SkillClass:
        var = chgen.skill_classes[skcls]
        val = ch.skills.aptitudes[skcls] = model[var].as_long()
        for skill in skcls.skills():
            val = model[chgen.skills[skill]]
            val_pb = model[chgen.skills_pb[skill]].as_long()
            val_free = model[chgen.skills_free[skill]].as_long()
            val_exp = model[chgen.skills_exp[skill]].as_long()
            val_cost = model[chgen.costs_exp[skill]].as_long()
            
            ch.skills.stats[skill].base_points = val_pb 
            ch.skills.stats[skill].free_points = val_free
            ch.skills.stats[skill].exp_points = val_exp
            ch.skills.stats[skill].experience_cost = val_cost 

            assert(ch.skills.stats[skill].value == val.as_long())

    for trait in Traits:
        ch.traits[trait] = traitlib.get_trait(model[chgen.traits[trait]].as_long())

    for gear in Gear:
        ch.gear[gear] = gearlib.get_gear(model[chgen.gear[gear]].as_long())
   

    ch.finalize()
    return ch





def negate_model(model):
    clauses = []
    for variable in model:
        value = model[variable]
        clauses.append(z3.Not(variable.as_ast() == int(value.as_long())))

    return z3.Or(*clauses)


def generate_character(count=1,novice=False,constraints=[],experience=15):
    pointbuy = 14
    freepoints = 10
    chgen = Z3CharGen()

    
    chgen.cstr(chgen.int_points == pointbuy)
    chgen.cstr(chgen.skill_points == freepoints)
    chgen.cstr(chgen.experience == experience)

    # Set the random seed
    z3.set_option('smt.arith.random_initial_value', True)
    z3.set_option('auto_config', False)
    z3.set_option('smt.phase_selection', 5)
    z3.set_option('smt.random_seed', random.randint(0,655356))



    # add user-provided constraints
    
    model = None
    for _ in range(count):
    
        solver = z3.Solver()
        chgen.user_cstrs = []
        for c in constraints:
            c.apply(chgen)

        solver.add(chgen.cstrs)
        solver.add(chgen.user_cstrs)

        result = solver.check()
        if result == z3.sat:
            model = solver.model()
            name = names.get_full_name()
            char = model_to_character(name,chgen,model)
            char.novice = novice
            yield char

            solver.add(negate_model(model))
        else:
            print("[[STOPPED EARLY]] Cannot generate any more characters that satisfy the provided constraints")
            return