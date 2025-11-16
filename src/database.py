from sqlalchemy import create_engine, func, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from typing import List, Optional
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Visit(Base):
    __tablename__ = "visits"

    id       = mapped_column(Integer, primary_key=True, autoincrement=True)
    date     = mapped_column(DateTime(timezone=False), insert_default=func.now(), nullable=False)
    user     = mapped_column(String, nullable=False)
    activity = mapped_column(ForeignKey("activities.id"), nullable=False)
    machine  = mapped_column(ForeignKey("machines.id"), nullable=True)
    material = mapped_column(ForeignKey("materials.id"), nullable=True)
    workshop = mapped_column(ForeignKey("workshops.id"), nullable=True)

class Activity(Base):
    __tablename__ = "activities"

    id        = mapped_column(Integer, primary_key=True, autoincrement=True)
    name      = mapped_column(String,  unique=True, nullable=False)
    machine   = mapped_column(Boolean, default=False)
    material  = mapped_column(Boolean, default=False)
    workshop  = mapped_column(Boolean, default=False)
    available = mapped_column(Boolean, default=True)
    
class Machine(Base):
    __tablename__ = "machines"

    id        = mapped_column(Integer, primary_key=True, autoincrement=True)
    name      = mapped_column(String, nullable=False)
    activity  = mapped_column(ForeignKey("activities.id"), nullable=False)
    available = mapped_column(Boolean, default=True)

class Material(Base):
    __tablename__ = "materials"

    id        = mapped_column(Integer, primary_key=True, autoincrement=True)
    name      = mapped_column(String, nullable=False)
    activity  = mapped_column(ForeignKey("activities.id"), nullable=False)
    available = mapped_column(Boolean, default=True)

class Workshop(Base):
    __tablename__ = "workshops"

    id        = mapped_column(Integer, primary_key=True, autoincrement=True)
    name      = mapped_column(String, nullable=False)
    activity  = mapped_column(ForeignKey("activities.id"), nullable=False)
    available = mapped_column(Boolean, default=True)


class Database():
    def __init__(self, connection, debug=False):
        self.engine = create_engine(connection, echo=debug)
        Base.metadata.create_all(self.engine, checkfirst=True)   
        self.session = sessionmaker(bind=self.engine)()

    def __del__(self):
        self.session.close()

    def getAllActivities(self, onlyActive=False):
        result = self.session.query(Activity.id, Activity.name)
        if onlyActive:
            result = result.where(Activity.available==True)
        result = result.all()
        self.session.close()
        return result

    def getActivity(self, activity):
        result = self.session.query(Activity).where(Activity.id==activity).one()
        self.session.close()
        self.session.close()
        return result

    def getAllMachines(self):
        result = self.session.query(Machine.id, Machine.name).all()
        self.session.close()
        return result

    def getActivityMachines(self, activity):
        result = self.session.query(Machine.id, Machine.name).where(Machine.activity==activity).all()
        self.session.close()
        return result

    def getAllMaterials(self):
        result = self.session.query(Material.id, Material.name).all()
        self.session.close()
        return result

    def getActivityMaterials(self, activity):
        result = self.session.query(Material.id, Material.name).where(Material.activity==activity).all()
        self.session.close()
        return result

    def getActivityWorkshops(self, activity):
        result = self.session.query(Workshop.id, Workshop.name).where(Workshop.activity==activity).all()
        self.session.close()
        return result

    def getSignInHistory(self):
        result = self.session.query(Visit.date, Visit.user, Activity.name, Machine.name, Material.name, Workshop.name
                                   ).join(Activity, Visit.activity==Activity.id
                                   ).join(Machine, Visit.machine==Machine.id, isouter=True
                                   ).join(Material, Visit.material==Material.id, isouter=True
                                   ).join(Workshop, Visit.workshop==Workshop.id, isouter=True
                                   ).all()
        self.session.close()
        return result
    
    def signin(self, date, user, activity, machine, material, workshop):
        self.session.begin()
        try:
            self.session.add(Visit(date=datetime.strptime(date, '%Y-%m-%dT%H:%M'), user=user, activity=activity, machine=machine, material=material, workshop=workshop))
        except Exception as e:
            print(e)
            self.session.rollback()
            return False
        else:
            self.session.commit()
        self.session.close()

        return True


