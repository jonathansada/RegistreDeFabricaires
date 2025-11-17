from .database import *

class RegFab():
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