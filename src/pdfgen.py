import pdfrw
from src.character import Intelligences, Skill, OtherStats, Traits, Gear

class PDFGenerator:

    def __init__(self):
        self.fields = {}
        self.ints = {}
        self.skills = {}
        self.define_bubbles()

    def define_bubbles(self):
        base = 11
        stride = 8

        offset = base
        self.ints[Intelligences.Kinesthetic] = (offset,offset+stride)
        offset += stride
        self.ints[Intelligences.Linguistic] = (offset,offset+stride)
        offset += stride
        self.ints[Intelligences.Spatial] = (offset,offset+stride)
        offset += stride
        self.ints[Intelligences.Logical] = (offset,offset+stride)
        offset += stride
        self.ints[Intelligences.Intrapersonal] = (offset,offset+stride)
        offset += stride
        self.ints[Intelligences.Interpersonal] = (offset,offset+stride)
        offset += stride
        self.ints[Intelligences.Musical] = (offset,offset+stride)
        offset += stride

        self.skills[Skill.Persuasion] = (offset,offset+stride)
        offset += stride
        self.skills[Skill.Empathy] = (offset,offset+stride)
        offset += stride
        self.skills[Skill.Deception] = (offset,offset+stride)
        offset += stride


        self.skills[Skill.Mysteries] = (offset,offset+stride)
        offset += stride
        self.skills[Skill.Artistry] = (offset,offset+stride)
        offset += stride
        self.skills[Skill.Academics] = (offset,offset+stride)
        offset += stride

        self.skills[Skill.Guns] = (offset,offset+stride)
        offset += stride
        self.skills[Skill.Brawling] = (offset,offset+stride)
        offset += stride
        self.skills[Skill.BattleSpeed] = (offset,offset+stride)
        offset += stride


        self.skills[Skill.MuscleTraining] = (offset,offset+stride)
        offset += stride
        self.skills[Skill.Endurance] = (offset,offset+stride)
        offset += stride
        self.skills[Skill.Agility] = (offset,offset+stride)
        offset += stride


        self.skills[Skill.Software] = (offset,offset+stride)
        offset += stride
        self.skills[Skill.Pilot] = (offset,offset+stride)
        offset += stride
        self.skills[Skill.Hardware] = (offset,offset+stride)
        offset += stride


        self.skills[Skill.Stealth] = (offset,offset+stride)
        offset += stride
        self.skills[Skill.Perception] = (offset,offset+stride)
        offset += stride
        self.skills[Skill.Drive] = (offset,offset+stride)
        offset += stride


        self.skills[Skill.Grit] = (offset,offset+stride)
        offset += stride
        self.skills[Skill.Intimidation] = (offset,offset+stride)
        offset += stride
        self.skills[Skill.Psyche] = (offset,offset+stride)
        offset += stride



    def register_checkbox(self,name,chb):
        self.fields[name] = chb

    def register_textfield(self,name,chb):
        self.fields[name] = chb

    def check(self,chb):
        val_str = pdfrw.objects.pdfname.BasePdfName('/Yes')
        chb.update(pdfrw.PdfDict(V=val_str, AS=val_str))
        
    def set_text(self,fld,value):
        text = '{}'.format(str(value))
        #fld.update(pdfrw.PdfDict(AP=text, V=text))
        fld.update(pdfrw.PdfDict(V=text))

    def flatten_pdf(self):
        for annotation in self.fields.values():
            annotation.update(pdfrw.PdfDict(F=4))

    def scan_fields(self,pdf):
        annotations = pdf.pages[0]['/Annots']
        for annotation in annotations:
            if annotation['/Subtype'] == '/Widget' and '/T' in annotation:
                field_name = annotation['/T'][1:-1]
                if "Check Box" in field_name:
                    self.register_checkbox(field_name, annotation)
                else:
                    self.register_textfield(field_name,annotation)
                    
    
    def print_field_names(self):
        for fld in self.fields.keys():
            print(fld)

    def stat_text_field(self,stat):
        if stat == OtherStats.Move:
            return self.fields["Move"]
        elif stat == OtherStats.Run:
            return self.fields["Run"]
        elif stat == OtherStats.Strength:
            return self.fields["Strength"]
        elif stat == OtherStats.Toughness:
            return self.fields["Toughness"]
        elif stat == OtherStats.Torso:
            return self.fields["Torso HP"]

    def trait_text_field(self,trait):
        if trait == Traits.Trait1:
            return self.fields["Background Trait #1"], self.fields["Background Trait #1 Description"]
        if trait == Traits.Trait2:
            return self.fields["Background Trait #2"], self.fields["Background Trait #2 Description"]
        if trait == Traits.Trait3:
            return self.fields["Background Trait #3"], self.fields["Background Trait #3 Description"]

        raise NotImplementedError

    def gear_text_field(self,gear):
        if gear == Gear.Gear1:
            return self.fields["Gear Line 1"]
        elif gear == Gear.Gear2:
            return self.fields["Gear Line 2"]
        elif gear == Gear.Gear3:
            return self.fields["Gear Line 3"]
        elif gear == Gear.Gear4:
            return self.fields["Gear Line 4"]
        elif gear == Gear.Gear5:
            return self.fields["Gear Line 5"]


    def license_text_field(self,license):
        templ = "License or Proficiency #%d"

   

    def intelligence_checkboxes(self,intel):
        minv,maxv = self.ints[intel]
        for i in range(minv,maxv):
            yield self.fields["Check Box %d" % i]

    def skill_checkboxes(self,skill):
        minv,maxv = self.skills[skill]
        for i in range(minv,maxv):
            yield self.fields["Check Box %d" % i]

    def save(self,name,pdf):
        pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject("true")))
        pdfrw.PdfWriter().write(name, pdf)

    def populate(self, templname,character):
        template_pdf = pdfrw.PdfReader(templname)
        self.scan_fields(template_pdf)

        self.set_text(self.fields["Character Name"], character.name)

        for trait in Traits:
            fld,fld_desc = self.trait_text_field(trait)
            self.set_text(fld, character.traits[trait])
        
        for gear in Gear:
            fld = self.gear_text_field(gear)
            self.set_text(fld, character.gear[gear])
 
        for intel,val in character.intelligences.stats.items():
            for idx, intchb in enumerate(self.intelligence_checkboxes(intel)):
                if(idx <= val-1):
                    self.check(intchb)

        for skcls,skills in character.skills.stats.items():
            for skill,val in skills.items():
                for idx, skchb  in enumerate(self.skill_checkboxes(skill)):
                    if(idx <= val-1):
                        self.check(skchb)

        for other,value in character.other.items():
            fld = self.stat_text_field(other)
            self.set_text(fld,value)


        return template_pdf
