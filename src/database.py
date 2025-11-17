from sqlalchemy import create_engine, func, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from typing import List, Optional
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Visit(Base):
    __tablename__ = "visits"

    id            = mapped_column(Integer, primary_key=True, autoincrement=True)
    date          = mapped_column(DateTime(timezone=False), insert_default=func.now(), nullable=False)
    name          = mapped_column(String, nullable=False)
    surname       = mapped_column(String, nullable=False)
    activity      = mapped_column(ForeignKey("activities.id"), nullable=False)
    machine       = mapped_column(ForeignKey("machines.id"), nullable=True)
    material      = mapped_column(ForeignKey("materials.id"), nullable=True)
    visit_length  = mapped_column(Integer, nullable=False) # Time the user has been in the fabrication space
    machine_usage = mapped_column(Integer, nullable=True) # Time the user has been using the machine
    description   = mapped_column(String, nullable=True)

class Activity(Base):
    __tablename__ = "activities"

    id        = mapped_column(Integer, primary_key=True, autoincrement=True)
    name      = mapped_column(String,  unique=True, nullable=False)
    machine   = mapped_column(Boolean, default=False)
    material  = mapped_column(Boolean, default=False)
    order     = mapped_column(Integer)
    
class Machine(Base):
    __tablename__ = "machines"

    id        = mapped_column(Integer, primary_key=True, autoincrement=True)
    name      = mapped_column(String, nullable=False)
    activity  = mapped_column(ForeignKey("activities.id"), nullable=False)
    order     = mapped_column(Integer)

class Material(Base):
    __tablename__ = "materials"

    id        = mapped_column(Integer, primary_key=True, autoincrement=True)
    name      = mapped_column(String, nullable=False)
    order     = mapped_column(Integer)

class VisitLength(Base):
    __tablename__ = "visit_lengths"

    id          = mapped_column(Integer, primary_key=True, autoincrement=True)
    description = mapped_column(String,  unique=True, nullable=False) 
    hours       = mapped_column(Integer) 


class MachineUsage(Base):
    __tablename__ = "visit_usages"

    id          = mapped_column(Integer, primary_key=True, autoincrement=True)
    description = mapped_column(String,  unique=True, nullable=False) 
    hours       = mapped_column(Integer) 




