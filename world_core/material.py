# world_core/material.py

class Material:
    def __init__(self, name, hardness, elasticity, opacity):
        self.name = name
        self.hardness = hardness
        self.elasticity = elasticity
        self.opacity = opacity


# Common materials
GRASS = Material("grass", hardness=0.2, elasticity=0.6, opacity=0.9)
WOOD  = Material("wood",  hardness=0.6, elasticity=0.3, opacity=0.95)
STONE = Material("stone", hardness=0.9, elasticity=0.05, opacity=1.0)