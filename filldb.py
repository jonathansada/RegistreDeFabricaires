import os
from dotenv import load_dotenv

from sqlalchemy import create_engine, func, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from typing import List, Optional

from src.database import Base, Visit, Activity, Machine, Material

load_dotenv()
engine = create_engine(os.getenv('DB_CON_STRING'), echo=True)
Session = sessionmaker(bind=engine)
session = Session()

#Fill DB with test data
Base.metadata.create_all(engine)

# Avtivities
session.add(Activity(name="Impressió 3D - Filament", machine=True,  material=True, id=1))
session.add(Activity(name="Impressió 3D - Resina",   machine=False, material=True, id=2))
session.add(Activity(name="Viniladora",              machine=False, material=True, id=3))
session.add(Activity(name="Tall Laser",              machine=False, material=True, id=4))
session.add(Activity(name="Termoformadora",          machine=False, material=True, id=5))
session.add(Activity(name="Robotica i Elèctronica",  machine=False, material=False, id=6))
session.add(Activity(name="Escaner 3D",              machine=False, material=False, id=7))
session.add(Activity(name="Altres",                  machine=False, material=False, id=8))

# Machines
session.add(Machine(name="Prusa i3 Mk3", activity=1))
session.add(Machine(name="Ender3 v2", activity=1))
session.add(Machine(name="Bambu Lab X1C", activity=1))

# Materials
session.add(Material(name="Propi, del usuari"))
session.add(Material(name="Material de l'EspluLab"))

session.commit()