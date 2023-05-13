from enum import Enum
from src.character import Skill, Intelligences

class Priority(Enum):
    Any = "any"
    Critical = "critical"
    High = "high"


# these rolls are critical ofr being successful
def get_critical_rolls():
    yield Intelligences.Kinesthetic, Skill.Brawling
    yield Intelligences.Spatial, Skill.Guns

# combinations
def get_high_priority_rolls():
    yield Intelligences.Interpersonal, Skill.Empathy
    yield Intelligences.Interpersonal, Skill.Persuasion
    yield Intelligences.Interpersonal, Skill.Deception

    yield Intelligences.Intrapersonal, Skill.Mysteries
    yield Intelligences.Intrapersonal, Skill.Psyche

    yield Intelligences.Spatial, Skill.Perception
    yield Intelligences.Spatial, Skill.Artistry
    yield Intelligences.Spatial, Skill.Guns


    yield Intelligences.Musical, Skill.Perception
    yield Intelligences.Musical, Skill.Artistry

    yield Intelligences.Logical, Skill.Academics
    yield Intelligences.Logical, Skill.Software
    yield Intelligences.Logical, Skill.Hardware

    yield Intelligences.Kinesthetic, Skill.MuscleTraining
    yield Intelligences.Kinesthetic, Skill.Guns
    yield Intelligences.Kinesthetic, Skill.Drive
    yield Intelligences.Kinesthetic, Skill.Agility
    yield Intelligences.Kinesthetic, Skill.Brawling

def get_rolls(priority):
    if priority.Any:
        return list(get_critical_rolls()) + list(get_high_priority_rolls())
    elif priority.Critical:
        return list(get_critical_rolls())
    elif priority.High:
        return list(get_high_priority_rolls())



