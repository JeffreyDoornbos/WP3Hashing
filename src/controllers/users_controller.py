from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import UserModel
from argon2 import PasswordHasher
from .controller import Controller

class UsersController(Controller):
    def __init__(self, cfg):
        super().__init__(cfg)
        self._model = UserModel()
        self.ph = PasswordHasher()

    def add_routes(self, app):
        self._blueprint = Blueprint('users_blueprint', __name__, template_folder='../templates/profiel')
        self.blueprint.add_url_rule('/profielbeheer', view_func=self.profielbeheer, methods=['GET', 'POST'])
        self.blueprint.add_url_rule('/profiel_ervaringsdeskundigen', view_func=self.profiel_ervaringsdeskundigen,
                                    methods=['GET'])
        self.blueprint.add_url_rule('/register', view_func=self.register, methods=['GET', 'POST'])
        self.blueprint.add_url_rule('/nieuwe_gebruiker_ervaringsdeskundigen', view_func=self.register,
                                    methods=['GET', 'POST'])
        self.blueprint.add_url_rule('/login', view_func=self.login, methods=['GET', 'POST'])
        app.register_blueprint(self.blueprint)
        return self.blueprint

    def profielbeheer(self):
        if request.method == 'POST':
            data = {
                'voornaam': request.form.get('voornaam'),
                'achternaam': request.form.get('achternaam'),
                'postcode': request.form.get('postcode'),
                'geslacht': request.form.get('geslacht'),
                'email': request.form.get('emailadres'),
                'telefoonnr': request.form.get('telefoonnummer'),
                'geboorte_datum': request.form.get('geboortedatum'),
                'type_beperking': request.form.get('type_beperking'),
                'gebruikte_hulpmiddelen': request.form.get('gebruikte_hulpmiddelen'),
                'kort_voorstellen': request.form.get('kort_voorstellen'),
                'bijzonderheden': request.form.get('bijzonderheden'),
                'akkoord_voorwaarden': request.form.get('akkoord_voorwaarden', 0),
                # TODO: Uncomment and implement guardian fields
                # 'heeft_toezichthouder': 1 if has_guardian else 0,
                # 'toezichthouder_naam': guardian_name,
                # 'toezichthouder_email': guardian_email,
                # 'toezichthouder_telefoon': guardian_phone,
                'voorkeur_benadering': request.form.get('voorkeur_benadering'),
                'type_onderzoek': request.form.get('type_onderzoek'),
                'bijzonderheden_beschikbaarheid': request.form.get('bijzonderheden_beschikbaarheid')
            }
            self.model.update_user(data)
            flash("User updated successfully", "success")
            return redirect(url_for('users_blueprint.profielbeheer'))
        else:
            user_id = session.get('user_id')
            if not user_id:
                flash("User not logged in", "danger")
                return redirect(url_for('users_blueprint.login'))
            user = self.model.get_user(user_id)
            return render_template('profiel/profielbeheer.html', user=user)

    def register(self):
        if request.method == 'POST':
            password = request.form.get('password')
            hashed_password = self.ph.hash(password)
            salt = ''
            data = {
                'voornaam': request.form.get('voornaam'),
                'achternaam': request.form.get('achternaam'),
                'postcode': request.form.get('postcode'),
                'geslacht': request.form.get('geslacht'),
                'telefoonnr': request.form.get('telefoonnummer'),
                'email': request.form.get('email'),
                'wachtwoord': hashed_password,
                'salt': salt,
                'geboorte_datum': request.form.get('geboortedatum'),
                'gebruikte_hulpmiddelen': request.form.get('gebruikte_hulpmiddelen'),
                'kort_voorstellen': request.form.get('kort_voorstellen'),
                'bijzonderheden': request.form.get('bijzonderheden'),
                'voorwaarden': request.form.get('akkoord_voorwaarden', 0),
                # TODO: Uncomment and implement guardian fields
                # 'heeft_toezichthouder': 1 if has_guardian else 0,
                # 'toezichthouder_naam': guardian_name,
                # 'toezichthouder_email': guardian_email,
                # 'toezichthouder_telefoon': guardian_phone,
                'voorkeur_benadering': request.form.get('voorkeur_benadering'),
                'type_onderzoek': request.form.get('type_onderzoek'),
                'bijzonderheden_beschikbaarheid': request.form.get('bijzonderheden_beschikbaarheid'),
                'status_id': 3
            }
            user_id = self.model.create_user(data)
            session['user_id'] = user_id
            flash("User registered successfully", "success")
            return redirect(url_for('users_blueprint.login'))
        else:
            return render_template('aanvragen_pagina(ervaringsdeskundigen)/nieuwe_gebruiker_ervaringsdeskundigen.html')

    def login(self):
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')

            # Check if it's an AJAX request
            is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

            user = self.model.get_user_by_email(email)

            if not user:
                if is_ajax:
                    return {'success': False, 'error': 'Onbekend email of wachtwoord'}, 404
                flash("Invalid email or password", "danger")
                return render_template('login/login.html')

            # Check if the user account is approved
            if user.get('status_id') != 1:
                if is_ajax:
                    return {'success': False, 'error': 'Je account is nog niet goedgekeurd'}, 403
                flash("Your account is not yet approved", "warning")
                return render_template('login/login.html')

            try:
                if self.ph.verify(user['wachtwoord'], password):
                    session['user_id'] = user['id']
                    session['user_type'] = 'beheerder' if 'beheerder' in user else 'ervaringsdeskundige'

                    if is_ajax:
                        return {'success': True,
                                'redirect': url_for('ervaringsdeskundige_blueprint.lopende_onderzoeken_ervaringsdeskundigen')}, 200

                    flash("Logged in successfully", "success")
                    return redirect(url_for('ervaringsdeskundige_blueprint.lopende_onderzoeken_ervaringsdeskundigen'))
                else:
                    if is_ajax:
                        return {'success': False, 'error': 'Onbekend email of wachtwoord'}, 401
                    flash("Invalid email or password", "danger")
            except Exception:
                if is_ajax:
                    return {'success': False, 'error': 'Onbekend email of wachtwoord'}, 401
                flash("Invalid email or password", "danger")

        return render_template('login/login.html')

    def profiel_ervaringsdeskundigen(self):
        user_id = session.get('user_id')
        if not user_id:
            flash("User not logged in", "danger")
            return redirect(url_for('users_blueprint.login'))

        user = self.model.get_user(user_id)
        return render_template('aanvragen_pagina(ervaringsdeskundigen)/profiel_ervaringsdeskundigen.html', user=user)