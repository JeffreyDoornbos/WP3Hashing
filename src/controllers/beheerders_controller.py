from os import urandom
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.beheerders_model import BeheerdersModel
import bleach
import base64
from argon2 import PasswordHasher
from threading import Timer
from .controller import Controller

class BeheerdersController(Controller):
    def __init__(self, cfg):
        super().__init__(cfg)
        self._model = BeheerdersModel()

        self.__SECOND_INTERVAL = 30.0
        self.__status_count_map = {}

        self.start_update_loop()

    def add_routes(self, app):
        self._blueprint = Blueprint("beheerders_blueprint", __name__, template_folder="../templates/beheerder")
        
        @self.blueprint.route("/beheerdersdashboard", methods=["GET"])
        def dashboard():
            if not session.get('beheerder_id'):
                return redirect(url_for('beheerders_blueprint.login_beheerder'))
            onderzoeken_in_afwachting = self.model.get_onderzoeken_in_afwachting()
            onderzoeken_afgekeurd = self.model.get_onderzoeken_afgekeurd()
            return render_template(
                "beheerdersdashboard.html",
                onderzoeken_in_afwachting=onderzoeken_in_afwachting,
                onderzoeken_afgekeurd=onderzoeken_afgekeurd
            )
        
        @self.blueprint.route("/update_status/<int:onderzoek_id>", methods=["POST"])
        def update_status(onderzoek_id):
            new_status = request.form.get("status")
            if new_status == "approved":
                status_id = 1  
            elif new_status == "rejected":
                status_id = 2  
            else:
                status_id = 3 
            self.model.update_onderzoek_status(onderzoek_id, status_id)
            flash("Onderzoek status bijgewerkt", "success")
            return redirect(url_for("beheerders_blueprint.dashboard"))
        
        @self.blueprint.route("/goedkeurendeelname", methods=["GET"])
        def deelname():
            return render_template("goedkeurendeelname.html")

        @self.blueprint.route("/goedkeurenervaringsdeskundigen", methods=["GET"])
        def goedkeuren_ervaringsdeskundigen():
            ervaringsdeskundigen_in_afwachting = self.model.get_ervaringsdeskundigen_in_afwachting()
            ervaringsdeskundigen_afgekeurd = self.model.get_ervaringsdeskundigen_afgekeurd()
            return render_template("goedkeurenervaringsdeskundigen.html",
                                   ervaringsdeskundigen_in_afwachting=ervaringsdeskundigen_in_afwachting,
                                   ervaringsdeskundigen_afgekeurd=ervaringsdeskundigen_afgekeurd)

        @self.blueprint.route("/update_ervaringsdeskundige_status/<int:ervaringsdeskundige_id>", methods=["POST"])
        def update_ervaringsdeskundige_status(ervaringsdeskundige_id):
            new_status = request.form.get("status")
            status_id = 1 if new_status == "approved" else 2 if new_status == "rejected" else 3
            self.model.update_ervaringsdeskundige_status(ervaringsdeskundige_id, status_id)
            flash("Status van ervaringsdeskundige bijgewerkt", "success")
            return redirect(url_for("beheerders_blueprint.goedkeuren_ervaringsdeskundigen"))
        
        @self.blueprint.route("/update_deelnamen_status/<int:deelname_id>", methods=["POST"])
        def update_deelnamen_status(deelname_id):
            new_status = request.form.get("status")
            status_id = 1 if new_status == 'approved' else 2 if new_status == 'rejected' else 3
            self.model.update_deelnamen_status(deelname_id, status_id)
            flash("Status van deelname bijgewerkt", "success")
            return redirect(url_for("beheerders_blueprint.deelname"))
        
        @self.blueprint.route("/beheerder_registratie/", methods=["GET", "POST"])
        def register_beheerder():
            if session.get('beheerder_id'):
                return redirect(url_for('beheerders_blueprint.dashboard'))
            if request.method == "POST":
                salt = base64.b64encode(urandom(16)).decode('utf-8')

                voornaam = bleach.clean(request.form.get('voornaam'), ['b', 'i', 'u', 'a'], strip=True)
                achternaam = bleach.clean(request.form.get('achternaam'), ['b', 'i', 'u', 'a'], strip=True)
                postcode = bleach.clean(request.form.get('postcode'), ['b', 'i', 'u', 'a'], strip=True)
                geslacht = bleach.clean(request.form.get('geslacht'), ['b', 'i', 'u', 'a'], strip=True)
                telefoonnr = bleach.clean(request.form.get('telefoonnr'), ['b', 'i', 'u', 'a'], strip=True)
                email = bleach.clean(request.form.get('email'), ['b', 'i', 'u', 'a'], strip=True)
                wachtwoord = bleach.clean(request.form.get('wachtwoord'), ['b', 'i', 'u', 'a'], strip=True)

                ph = PasswordHasher()
                hashed_password = ph.hash(wachtwoord + salt)

                data = (voornaam, achternaam, postcode, geslacht, telefoonnr, email, hashed_password, salt)
                id = self.model.create_beheerder(data)

                if not id:
                    flash("Failed to create beheerder", "error")
                    return {"error": "Failed to create beheerder"}, 500

                session['beheerder_id'] = id
                return redirect(url_for('beheerders_blueprint.login_beheerder'))

            return render_template("register.html")

        @self.blueprint.route("/beheerder_login/", methods=["GET", "POST"])
        def login_beheerder():
            if session.get('beheerder_id'):
                return redirect(url_for('beheerders_blueprint.dashboard'))

            if request.method == "POST":
                email = bleach.clean(request.form.get('email'), ['b', 'i', 'u', 'a'], strip=True)
                password = bleach.clean(request.form.get('wachtwoord'), ['b', 'i', 'u', 'a'], strip=True)

                ww = self.model.get_beheerder_password(email)
                if ww and 'wachtwoord' in ww and 'salt' in ww:
                    ph = PasswordHasher()
                    try:

                        ph.verify(ww['wachtwoord'], password + ww['salt'])
                        session['beheerder_id'] = ww['id']
                        return redirect(url_for('beheerders_blueprint.dashboard'))
                    except Exception:
                        flash("Incorrect wachtwoord", "error")
                        return {"error": "Incorrect password"}, 500

                flash("Beheerder niet gevonden", "error")
                return {"error": "Beheerder niet gevonden"}, 404

            return render_template("login.html")

        @self.blueprint.route("/beheerder_logout/", methods=["GET"])
        def logout_beheerder():
            session.pop('beheerder_id')
            return redirect(url_for('beheerders_blueprint.login_beheerder'))
        
        @self.blueprint.route("/poll/", methods=["GET"])
        def poll_status():
            table = bleach.clean(request.args.get('table', type=str), ['b', 'i', 'u', 'a'], strip=True)
            status = request.args.get('status', type=int) # not mucht to clean here, it gets converted to int and if it's not an int it throws an error
            if not table or not status:
                return {'error': 'Missing required argument'}, 400
            count = self.__status_count_map[table][status] if table in self.__status_count_map and status in self.__status_count_map[table] else 0
            return {'data': count}, 200

        @self.blueprint.route("/render_table/<table>/<int:status>/", methods=["GET"])
        def render_table(table:str, status:int):
            match table:
                case 'onderzoeken':
                    return self.render_onderzoeken_table(status)
                case 'ervaringsdeskundigen':
                    return self.render_ervaringsdeskundigen_table(status)
                case 'deelnamen':
                    return self.render_deelnamen_table(status)
                

        app.register_blueprint(self.blueprint)
        return self.blueprint
    
    # This method starts the update loop, the update method executes the code
    def start_update_loop(self):
        # Run each update once at the start to prevent missing or stale data
        self.start_timer_for('onderzoeken', 3)
        self.start_timer_for('onderzoeken', 2)
        self.start_timer_for('ervaringsdeskundigen', 3)
        self.start_timer_for('ervaringsdeskundigen', 2)
        self.start_timer_for('deelnamen', 3)
        self.start_timer_for('deelnamen', 2)

    def start_timer_for(self, table:str, status_id:int):
        self.update(table, status_id)
        timer = Timer(self.__SECOND_INTERVAL, self.update, kwargs={'table': table, 'status': status_id})
        timer.start()
    
    # This method will run on a background thread and cache the database result 
    # which can be retrieved from the /poll/ endpoint
    def update(self, table:str, status:int):
        new = self.model.get_row_count_for(table, status)
        if new is not None:
            if not table in self.__status_count_map:
                self.__status_count_map[table] = {}
            self.__status_count_map[table][status] = new

    def render_onderzoeken_table(self, status:int):
        onderzoeken = []
        if status == 3:
            onderzoeken = self.model.get_onderzoeken_in_afwachting()
        elif status == 2:
            onderzoeken = self.model.get_onderzoeken_afgekeurd()
        else:
            return render_template("onderzoeken_table.html", status_id=0, onderzoeken=None), 200
        return render_template("onderzoeken_table.html", status_id=status, onderzoeken=onderzoeken), 200
    
    def render_ervaringsdeskundigen_table(self, status:int):
        ervaringsdeskundigen = []
        if status == 3:
            ervaringsdeskundigen = self.model.get_ervaringsdeskundigen_in_afwachting()
        elif status == 2:
            ervaringsdeskundigen = self.model.get_ervaringsdeskundigen_afgekeurd()
        else:
            return render_template("ervaringsdeskundigen_table.html", status_id=0, ervaringsdeskundigen=None), 200
        return render_template("ervaringsdeskundigen_table.html", status_id=status, ervaringsdeskundigen=ervaringsdeskundigen), 200


    def render_deelnamen_table(self, status:int):
        deelnamen = []
        if status == 3:
            deelnamen = self.model.get_deelnamen_in_afwachting()
        elif status == 2:
            deelnamen = self.model.get_deelnamen_afgekeurd()
        else:
            return render_template("deelnamen_table.html", status_id=0, deelnamen=None), 200
        return render_template("deelnamen_table.html", status_id=status, deelnamen=deelnamen), 200
