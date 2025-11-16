import os
from dotenv import load_dotenv

from flask import Flask, request, render_template, session, redirect, jsonify
from .src.database import Database

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET')

dbConnection = os.getenv('DB_CON_STRING')
debug = bool(os.getenv('DB_DEBUG'))

###########
# User Side
###########
@app.route("/", methods=['GET'])
@app.route('/checkin', methods=['GET', "POST"])
def chekin_get():
    if request.method == 'POST':
        date  = request.form['date']
        fname = request.form['fname']
        sname = request.form['sname']
        activity_id = request.form['activity']

        db = Database(connection=dbConnection, debug=debug)
        activity    = db.getActivity(activity_id)
        machine_id  = request.form['machine']   if activity.machine  else None
        material_id = request.form['material']  if activity.material else None
                
        result = db.signin(date, fname, sname, activity_id, machine_id, material_id)

        if result == True:
            return jsonify({"result":"success"})
        else:
            return jsonify({"result":"error"})
    else:
        db = Database(connection=dbConnection, debug=debug)
        return render_template('checkin_form.html', activities = db.getAllActivities())

@app.route('/getActivityDetails/<activity_id>', methods=['GET', "POST"])
def getActivityDetails(activity_id):
    answer = {"machines": False, "materials": False}

    db = Database(connection=dbConnection, debug=debug)

    activity = db.getActivity(activity_id)
    if activity.machine:
        answer["machines"] = [{"id":machine[0], "name": machine[1]} for machine in db.getActivityMachines(activity_id)]

    if activity.material:
        answer["materials"] = [{"id":material[0], "name": material[1]} for material in db.getAllMaterials()]

    return jsonify(answer)


############
# Admin Side
############
@app.route("/admin", methods=['GET', "POST"])
def admin():
    if request.method == 'POST':
        user     = request.form['user']
        password = request.form['password']

        if user==os.getenv('ADMIN_USER') and password==os.getenv('ADMIN_PASSWORD'):
            session['admin'] = True
        
        return redirect("/admin")
    else:
        if 'admin' in session:
            db = Database(connection=dbConnection, debug=debug)
            return render_template('admin_history.html', history = db.getSignInHistory())
        else:
            return render_template('admin_form.html')


@app.route("/admin/logout")
def admin_logout():
    if 'admin' in session:
        session.pop('admin', None)
    return redirect("/")