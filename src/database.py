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

class Database():
    def __init__(self, connection, debug=False):
        self.engine = create_engine(connection, echo=debug)
        Base.metadata.create_all(self.engine, checkfirst=True)   
        self.session = sessionmaker(bind=self.engine)()

    def __del__(self):
        self.session.close()

    def getAllActivities(self):
        result = self.session.query(Activity.id, Activity.name).order_by(Activity.order.asc(), Activity.name).all()
        self.session.close()
        return result

    def getActivity(self, activity):
        result = self.session.query(Activity).where(Activity.id==activity).one()
        self.session.close()
        self.session.close()
        return result

    def getAllVisitLengths(self):
        result = self.session.query(VisitLength.hours, VisitLength.description).order_by(VisitLength.hours.asc()).all()
        self.session.close()
        return result

    def getAllMachines(self):
        result = self.session.query(Machine.id, Machine.name).order_by(Machine.order.asc(), Machine.name).all()
        self.session.close()
        return result

    def getActivityMachines(self, activity):
        result = self.session.query(Machine.id, Machine.name).where(Machine.activity==activity).all()
        self.session.close()
        return result

    def getAllMachineUsages(self):
        result = self.session.query(MachineUsage.hours, MachineUsage.description).order_by(MachineUsage.hours).all()
        self.session.close()
        return result

    def getAllMaterials(self):
        result = self.session.query(Material.id, Material.name).order_by(Material.order.asc(), Material.name).all()
        self.session.close()
        return result

    def getSignInHistory(self):
        result = self.session.query(Visit.date, Visit.name,  Visit.surname, Activity.name, Machine.name, Material.name, Visit.visit_length, Visit.machine_usage
                                   ).join(Activity, Visit.activity==Activity.id
                                   ).join(Machine, Visit.machine==Machine.id, isouter=True
                                   ).join(Material, Visit.material==Material.id, isouter=True
                                   ).order_by(Visit.date).all()
        self.session.close()
        return result
    
    def signin(self, date, fname, sname, activity, visit_length, machine, machine_usage, material):
        self.session.begin()
        try:
            self.session.add(Visit(date = datetime.strptime(date, '%Y-%m-%dT%H:%M'), 
                                   name = fname, 
                                   surname = sname, 
                                   activity = activity, 
                                   machine = machine, 
                                   material = material, 
                                   visit_length = visit_length, 
                                   machine_usage = machine_usage))
        except Exception as e:
            print(e)
            self.session.rollback()
            return False
        else:
            self.session.commit()
        self.session.close()

        return True


