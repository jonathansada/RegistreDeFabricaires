from sqlalchemy import create_engine, func, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from typing import List, Optional

from src.database import Base, Visit, Activity, Machine, Material, Workshop

engine = create_engine('sqlite:///./data/db/esplulab.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

#Fill DB with test data
Base.metadata.create_all(engine)

# Avtivities
session.add(Activity(name="Impressió 3D",   machine=True,  material=True,  workshop=False, id=1))
session.add(Activity(name="Viniladora",     machine=False, material=True,  workshop=False, id=2))
session.add(Activity(name="Tall Laser",     machine=False, material=True,  workshop=False, id=3))
session.add(Activity(name="Termoformadora", machine=False, material=True,  workshop=False, id=4))
session.add(Activity(name="CafeLab",        machine=False, material=False, workshop=False, id=5))
session.add(Activity(name="EduLab",         machine=False, material=False, workshop=False, id=6))
session.add(Activity(name="CreaLab",        machine=False, material=False, workshop=False, id=7))
session.add(Activity(name="FamilyLab",      machine=False, material=False, workshop=False, id=8))
session.add(Activity(name="Taller",         machine=False, material=False, workshop=True,  id=9))

# Machines
session.add(Machine(name="Prusa i3 Mk3s 01", activity=1, available=True))
session.add(Machine(name="Prusa i3 Mk3s 02", activity=1, available=True))
session.add(Machine(name="Prusa i3 Mk3s 03", activity=1, available=True))
session.add(Machine(name="Prusa i3 Mk3s 04", activity=1, available=True))
session.add(Machine(name="Prusa i3 Mk3s 05", activity=1, available=True))
session.add(Machine(name="Prusa i3 Mk3s 06", activity=1, available=True))
session.add(Machine(name="Bambu Lab H2D",    activity=1, available=True))

# Materials
session.add(Material(name="Filament Propi", activity=1, available=True))
session.add(Material(name="Resina Propia",  activity=1, available=True))
session.add(Material(name="PLA Groc",       activity=1, available=True))
session.add(Material(name="PLA Blau",       activity=1, available=True))
session.add(Material(name="Resina Blava",   activity=1, available=True))
session.add(Material(name="Vinil Propi",    activity=2, available=True))
session.add(Material(name="Vinil Negre",    activity=2, available=True))
session.add(Material(name="Vinil Negre",    activity=2, available=True))
session.add(Material(name="Material Propi", activity=3, available=True))
session.add(Material(name="Fusta 3mm",      activity=3, available=True))
session.add(Material(name="Fusta 5mm",      activity=3, available=True))
session.add(Material(name="Metacrilat 3mm", activity=3, available=True))
session.add(Material(name="Material Propi", activity=4, available=True))

# Workshops
session.add(Workshop(name="Taller d'ivern", activity=1, available=True))

session.commit()