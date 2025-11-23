import os
from dotenv import load_dotenv

from flask import Flask, request, render_template, session, redirect, jsonify, make_response
try: # Production
    from src.regfab import RegFab
except: # Local
    from .src.regfab import RegFab

load_dotenv()
flask = Flask(__name__)
flask.secret_key = os.getenv('FLASK_SECRET')

app = RegFab(connection=os.getenv('DB_CON_STRING'), debug=bool(os.getenv('DB_DEBUG')))

###########
# User Side
###########
@flask.route("/", methods=['GET'])
@flask.route('/checkin', methods=['GET', "POST"])
def chekin_get():
    if request.method == 'POST':
        date        = request.form['date']
        fname       = request.form['fname']
        sname       = request.form['sname']
        activity_id = request.form['activity']
        visit_time  = request.form['visit_time']

        activity      = app.getActivity(activity_id)
        machine_id    = request.form['machine']       if activity.machine  else None
        machine_usage = request.form['machine_usage'] if activity.machine  else 0
        material_id   = request.form['material']      if activity.material else None
                
        result = app.signin(date, fname, sname, activity_id, visit_time, machine_id, machine_usage, material_id)

        if result == True:
            return jsonify({"result":"success"})
        else:
            return jsonify({"result":"error"})
    else:
        return render_template('checkin_form.html', activities = app.getAllActivities(), visit_lengths = app.getAllVisitLengths())

@flask.route('/getActivityDetails/<activity_id>', methods=['GET', "POST"])
def getActivityDetails(activity_id):
    answer = {"machines": False, "materials": False}
    activity = app.getActivity(activity_id)
    if activity.machine:
        answer["machines"]      = [{"id":machine[0], "name": machine[1]} for machine in app.getActivityMachines(activity_id)]
        answer["machine_usage"] = [{"id":usage[0],   "name": usage[1]}   for usage   in app.getAllMachineUsages()]

    if activity.material:
        answer["materials"] = [{"id":material[0], "name": material[1]} for material in app.getAllMaterials()]

    return jsonify(answer)


############
# Admin Side
############
@flask.route("/admin", methods=['GET', "POST"])
def admin():
    if request.method == 'POST':
        user     = request.form['user']
        password = request.form['password']

        if user==os.getenv('ADMIN_USER') and password==os.getenv('ADMIN_PASSWORD'):
            session['admin'] = True
        
        return redirect("/admin")
    else:
        if 'admin' in session:
            return render_template('admin_history.html', history = app.getSignInHistory())
        else:
            return render_template('admin_form.html')

@flask.route("/admin/export", methods=['GET'])
def admin_export():
    if 'admin' in session:
        resp = make_response(app.historyToCSV())
        resp.headers["Content-Disposition"] = "attachment; filename=regfab_export.csv"
        resp.headers["Content-Type"] = "text/csv"
        return resp
    else:
        return redirect("/admin")


@flask.route("/admin/logout")
def admin_logout():
    if 'admin' in session:
        session.pop('admin', None)
    return redirect("/")