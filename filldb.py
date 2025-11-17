import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database import *

load_dotenv()
engine = create_engine(os.getenv('DB_CON_STRING'), echo=True)
Session = sessionmaker(bind=engine)
session = Session()

#Fill DB with test data
Base.metadata.create_all(engine)

# Avtivities
session.add(Activity(name="Impressió 3D - Filament", machine=True,  material=True, id=1, order=1))
session.add(Activity(name="Impressió 3D - Resina",   machine=False, material=True, id=2, order=2))
session.add(Activity(name="Viniladora",              machine=False, material=True, id=3, order=3))
session.add(Activity(name="Tall Laser",              machine=False, material=True, id=4, order=4))
session.add(Activity(name="Termoformadora",          machine=False, material=True, id=5, order=5))
session.add(Activity(name="Robotica i Elèctronica",  machine=False, material=False, id=6, order=6))
session.add(Activity(name="Escaner 3D",              machine=False, material=False, id=7, order=7))
session.add(Activity(name="Altres",                  machine=False, material=False, id=8, order=8))

# Machines
session.add(Machine(name="Prusa i3 Mk3", activity=1, order=1))
session.add(Machine(name="Ender3 v2", activity=1, order=3))
session.add(Machine(name="Bambu Lab X1C", activity=1, order=2))

# Materials
session.add(Material(name="Propi, del usuari", order=1))
session.add(Material(name="Material de l'EspluLab", order=2))

# VisitLength
session.add(VisitLength(description="Menys de 1 hora",   hours=1))
session.add(VisitLength(description="Entre 1 i 2 hores", hours=2))
session.add(VisitLength(description="Entre 2 i 3 hores", hours=3))
session.add(VisitLength(description="Entre 3 i 4 hores", hours=4))
session.add(VisitLength(description="Més de 4 hores",    hours=5))
session.add(VisitLength(description="Tot el día",        hours=8))

# MachineUsage
session.add(MachineUsage(description="Menys de 1 hora",   hours=1))
session.add(MachineUsage(description="Entre 1 i 2 hores", hours=2))
session.add(MachineUsage(description="Entre 2 i 3 hores", hours=3))
session.add(MachineUsage(description="Entre 3 i 4 hores", hours=4))
session.add(MachineUsage(description="Entre 4 i 8 hores", hours=8))
session.add(MachineUsage(description="Entre 8 i 16 hores", hours=16))
session.add(MachineUsage(description="Entre 16 i 24 hores", hours=24))
session.add(MachineUsage(description="Entre 24 i 48 hores", hours=48))
session.add(MachineUsage(description="Més de 48 hores"    , hours=72))


session.commit()