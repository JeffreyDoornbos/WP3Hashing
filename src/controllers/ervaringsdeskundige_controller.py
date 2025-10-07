import os
import sqlite3
from flask import Blueprint, request, render_template, redirect, url_for, jsonify, session, g
from models.ervaringsdeskundige_model import Ervaringsdeskundige
from urllib.parse import urlencode


class ErvaringsdeskundigeController:
    def __init__(self, cfg):
        self.cfg = cfg
        self._blueprint = None

        # Get the base directory of the application
        base_dir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

        # Set default paths - can be overridden from config if needed
        self.db_path = os.path.join(base_dir, 'database', 'database.db')
        self.queries_path = os.path.join(base_dir, 'database', 'queries', 'queries.sql')

        # Override from config if provided
        if cfg and 'database_path' in cfg:
            self.db_path = cfg['database_path']
        if cfg and 'queries_path' in cfg:
            self.queries_path = cfg['queries_path']

        print(f"Using database at: {self.db_path}")
        print(f"Using queries at: {self.queries_path}")

    def get_db_connection(self):
        """Create and return a database connection"""
        try:
            # Make sure the directory exists
            db_dir = os.path.dirname(self.db_path)
            if not os.path.exists(db_dir):
                os.makedirs(db_dir)

            conn = sqlite3.connect(self.db_path)
            return conn
        except Exception as e:
            print(f"Failed to connect to database: {e}")
            raise

    def execute_query(self, query, params=None):
        """Execute a query and return results"""
        conn = None
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()

            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            result = cursor.fetchall()
            return result
        except Exception as e:
            print(f"Database error: {e}")
            raise
        finally:
            if conn:
                conn.close()

    def execute_query_one(self, query, params=None):
        """Execute a query and return single result"""
        conn = None
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()

            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            result = cursor.fetchone()
            return result
        except Exception as e:
            print(f"Database error: {e}")
            raise
        finally:
            if conn:
                conn.close()

    def execute_write_query(self, query, params=None):
        """Execute a write query (INSERT, UPDATE, DELETE)"""
        conn = None
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()

            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            conn.commit()
            return True
        except Exception as e:
            print(f"Database error: {e}")
            raise
        finally:
            if conn:
                conn.close()

    def get_current_user(self):
        """Get current user data"""
        try:
            ervaringsdeskundige = Ervaringsdeskundige()
            queries = ervaringsdeskundige.load_queries(self.queries_path)
            test_gebruiker = queries['test_gebruiker']

            user = self.execute_query_one(test_gebruiker)
            return user
        except Exception as e:
            print(f"Fout tijdens ophalen van de gebruiker: {e}")
            return None

    def get_queries(self):
        """Load all SQL queries"""
        ervaringsdeskundige = Ervaringsdeskundige()
        return ervaringsdeskundige.load_queries(self.queries_path)

    def check_deelname(self, user_id):
        """Check user participation in research"""
        queries = self.get_queries()
        check_deelname_query = queries['check_deelname']
        results = self.execute_query(check_deelname_query, (user_id,))
        return {row[0] for row in results}

    def add_routes(self, app):
        self._blueprint = Blueprint("ervaringsdeskundige_blueprint", __name__,
                                    template_folder="../templates/aanvragen_pagina(ervaringsdeskundigen)")

        @self._blueprint.before_request
        def load_logged_in_user():
            g.current_user = session.get('user_id')

        @self._blueprint.route('/process', methods=['POST'])
        def process():
            try:
                print("Ontvangen data:", request.form)

                lijst = [
                    "voornaam", "achternaam", "postcode", "geslacht",
                    "email", "telefoonnummer", "geboortedatum", "type_beperking",
                    "akkoord_voorwaarden", "toezichthouder", "naam_voogd_toezichthouder",
                    "e_mailadres_voogd_toezichthouder", "telefoonnummer_voogd_toezichthouder",
                    "voorkeur_benadering", "type_onderzoek", "bijzonderheden_beschikbaarheid",
                ]

                ontbrekende_namen = [naam for naam in lijst if not request.form.get(naam)]

                if ontbrekende_namen:
                    return jsonify({'error': f'Vul de volgende verplichte velden in: {", ".join(ontbrekende_namen)}'})

                return jsonify({'message': 'Formulier succesvol verzonden!'})

            except Exception as e:
                return jsonify({'error': str(e)})

        @self._blueprint.route("/nieuwe_gebruiker_ervaringsdeskundigen", methods=["GET", "POST"])
        def nieuwe_gebruiker_ervaringsdeskundigen():
            return render_template('nieuwe_gebruiker_ervaringsdeskundigen.html')

        @self._blueprint.route("/lopende_onderzoeken_ervaringsdeskundigen", methods=["GET", "POST"])
        def lopende_onderzoeken_ervaringsdeskundigen():
            user_id = g.current_user if g.current_user else None
            user = g.current_user if g.current_user else None

            if not user_id:
                return "Geen gebruiker ingelogd.", 401

            try:
                queries = self.get_queries()
                normal_query = queries['normal_query']
                count_query = queries['count_query']
                doelgroep_query = queries['doelgroep_query']

                # zoeken in de onderzoeken
                search = request.args.get("search", '').strip()
                doelgroep = request.args.get("doelgroep", '').strip()
                beschikbaar = request.args.get("beschikbaar", '').strip()

                # Pagination
                page = int(request.args.get('page', 1))
                per_page = 10
                start = (page - 1) * per_page

                user_id = user_id[0] if isinstance(user_id, tuple) else user_id
                deelnemende_onderzoeken = self.check_deelname(user_id)

                # Build query
                query = normal_query.replace("SELECT", "SELECT onderzoeken.id, ")
                parameters = []

                if search:
                    query += " HAVING onderzoeken.titel LIKE ?"
                    parameters.append(f"%{search}%")

                if doelgroep:
                    query += " HAVING GROUP_CONCAT(beperkingen.naam, ', ') LIKE ?"
                    parameters.append(f"%{doelgroep}%")

                if beschikbaar:
                    query += " HAVING onderzoeken.beschikbaar IS NOT 0 OR NULL"

                query += " LIMIT ? OFFSET ?"
                parameters.extend([per_page, start])

                onderzoeken = self.execute_query(query, parameters)

                # Get total count
                count_parameters = []
                if search:
                    count_query += " AND onderzoeken.titel LIKE ?"
                    count_parameters.append(f"%{search}%")

                if count_parameters:
                    totale_onderzoeken = self.execute_query_one(count_query, count_parameters)[0]
                else:
                    totale_onderzoeken = self.execute_query_one(count_query)[0]

                # Pagination logic
                total_pages = (totale_onderzoeken + per_page - 1) // per_page
                next_page = page + 1 if page < total_pages else None
                prev_page = page - 1 if page > 1 else None
                show_first = page > 1
                show_last = page < total_pages

                # URL parameters
                base_params = {
                    "search": search,
                    "doelgroep": doelgroep,
                    "beschikbaar": beschikbaar,
                }

                page_numbers = []
                for i in range(1, total_pages + 1):
                    base_params["page"] = i
                    page_numbers.append(f"?{urlencode(base_params)}")

                doelgroepen = [row[1] for row in self.execute_query(doelgroep_query)]

                return render_template(
                    'lopende_onderzoeken_ervaringsdeskundigen.html',
                    onderzoeken=onderzoeken,
                    page=page,
                    next_page=next_page,
                    prev_page=prev_page,
                    total_pages=total_pages,
                    page_numbers=page_numbers,
                    show_first=show_first,
                    show_last=show_last,
                    search=search,
                    doelgroep=doelgroep,
                    beschikbaar=beschikbaar,
                    doelgroepen=doelgroepen,
                    deelnemende_onderzoeken=deelnemende_onderzoeken,
                    user_id=user_id,
                    user=user,
                )

            except Exception as e:
                print(f"Fout tijdens het verwerken van de lopende onderzoeken: {e}")
                return "Interne serverfout", 500

        @self._blueprint.route("/filter_doelgroep_ervaringsdeskundigen", methods=["GET", "POST"])
        def filter_doelgroep_ervaringsdeskundigen():
            user_id = g.current_user if g.current_user else None
            user = g.current_user if g.current_user else None

            if not user_id:
                return "Geen gebruiker ingelogd.", 401

            try:
                queries = self.get_queries()
                doelgroepen_query = queries['doelgroepen']
                count_query = queries['counting_doelgroep']
                eigen_doelgroepen_query = queries['eigen_doelgroepen']

                # Search parameters
                search = request.args.get("search", '').strip()
                doelgroep = request.args.get("doelgroep", '').strip()
                beschikbaar = request.args.get("beschikbaar", '').strip()

                # Pagination
                page = int(request.args.get('page', 1))
                per_page = 10
                start = (page - 1) * per_page

                user_id = user_id[0] if isinstance(user_id, tuple) else user_id
                deelnemende_onderzoeken = self.check_deelname(user_id)

                # Build query
                query = doelgroepen_query
                parameters = [user_id]

                if search:
                    query += " HAVING onderzoeken.titel LIKE ?"
                    parameters.append(f"%{search}%")

                if doelgroep:
                    query += " HAVING GROUP_CONCAT(beperkingen.naam, ', ') LIKE ?"
                    parameters.append(f"%{doelgroep}%")

                if beschikbaar:
                    query += " HAVING onderzoeken.beschikbaar IS NOT 0 OR NULL"

                query += " LIMIT ? OFFSET ?"
                parameters.extend([per_page, start])

                onderzoeken = self.execute_query(query, parameters)

                # Count query
                count_parameters = [user_id]
                if search:
                    count_query += " AND onderzoeken.titel LIKE ?"
                    count_parameters.append(f"%{search}%")

                totale_onderzoeken = self.execute_query_one(count_query, count_parameters)[0]

                # Pagination logic
                total_pages = (totale_onderzoeken + per_page - 1) // per_page
                next_page = page + 1 if page < total_pages else None
                prev_page = page - 1 if page > 1 else None
                show_first = page > 1
                show_last = page < total_pages

                # URL parameters
                base_params = {
                    "search": search,
                    "doelgroep": doelgroep,
                    "beschikbaar": beschikbaar,
                }

                page_numbers = []
                for i in range(1, total_pages + 1):
                    base_params["page"] = i
                    page_numbers.append(f"?{urlencode(base_params)}")

                doelgroepen = [row[1] for row in self.execute_query(eigen_doelgroepen_query, (user_id,))]

                return render_template(
                    'filter_doelgroep_ervaringsdeskundigen.html',
                    onderzoeken=onderzoeken,
                    page=page,
                    next_page=next_page,
                    prev_page=prev_page,
                    total_pages=total_pages,
                    page_numbers=page_numbers,
                    show_first=show_first,
                    show_last=show_last,
                    search=search,
                    doelgroep=doelgroep,
                    beschikbaar=beschikbaar,
                    doelgroepen=doelgroepen,
                    deelnemende_onderzoeken=deelnemende_onderzoeken,
                    eigen_doelgroepen=doelgroepen,
                    user_id=user_id,
                    user=user,
                )

            except Exception as e:
                print(f"Fout tijdens het verwerken van mijn doelgroepen: {e}")
                return "Interne serverfout", 500


        # Filtert op deelnames
        @self._blueprint.route("/filter_deelnames_ervaringsdeskundigen", methods=["GET", "POST"])
        def filter_deelnames_ervaringsdeskundigen():
            user_id = g.current_user if g.current_user else None
            user = g.current_user if g.current_user else None

            if not user_id:
                return "Geen gebruiker ingelogd.", 401

            try:
                queries = self.get_queries()
                deelnames = queries['deelnames']
                counting_query = queries['counting_query']
                doelgroep_query = queries['doelgroep_query']

                # zoeken in de onderzoeken
                search = request.args.get("search", '').strip()
                doelgroep = request.args.get("doelgroep", '').strip()
                beschikbaar = request.args.get("beschikbaar", '').strip()

                # Dit is voor de pagina nummers
                page = int(request.args.get('page', 1))
                per_page = 10
                start = (page - 1) * per_page

                query = deelnames
                user_id = user_id[0] if isinstance(user_id, tuple) else user_id
                parameters = [user_id]

                deelnemende_onderzoeken = self.check_deelname(user_id)

                if search:
                    query += " AND onderzoeken.titel LIKE ?"
                    parameters.append(f"%{search}%")

                if doelgroep:
                    query += " HAVING GROUP_CONCAT(beperkingen.naam, ', ') LIKE ?"
                    parameters.append(f"%{doelgroep}%")

                if beschikbaar:
                    query += " AND onderzoeken.beschikbaar IS NOT 0 OR NULL"

                query += " LIMIT ? OFFSET ?"
                parameters.extend([per_page, start])

                onderzoeken = self.execute_query(query, parameters)

                count_parameters = [user_id]

                if search:
                    counting_query += " AND onderzoeken.titel LIKE ?"
                    count_parameters.append(f"%{search}%")

                totale_onderzoeken = self.execute_query_one(counting_query, count_parameters)[0]

                total_pages = (totale_onderzoeken + per_page - 1) // per_page
                next_page = page + 1 if page < total_pages else None
                prev_page = page - 1 if page > 1 else None

                show_first = page > 1
                show_last = page < total_pages

                base_params = {
                    "search": search,
                    "doelgroep": doelgroep,
                    "beschikbaar": beschikbaar,
                }

                page_numbers = []
                for i in range(1, total_pages + 1):
                    base_params["page"] = i
                    page_numbers.append(f"?{urlencode(base_params)}")

                doelgroepen = [row[1] for row in self.execute_query(doelgroep_query)]

                return render_template(
                    'filter_deelnames_ervaringsdeskundigen.html',
                    onderzoeken=onderzoeken,
                    page=page,
                    next_page=next_page,
                    prev_page=prev_page,
                    total_pages=total_pages,
                    page_numbers=page_numbers,
                    show_first=show_first,
                    show_last=show_last,
                    search=search,
                    doelgroep=doelgroep,
                    beschikbaar=beschikbaar,
                    doelgroepen=doelgroepen,
                    deelnemende_onderzoeken=deelnemende_onderzoeken,
                    user_id=user_id,
                    user=user,
                )

            except Exception as e:
                print(f"Fout tijdens het verwerken van mijn deelnames: {e}")
                return "Interne serverfout", 500

        @self._blueprint.route("/info_onderzoek_ervaringsdeskundigen", methods=["GET", "POST"])
        def info_onderzoek_ervaringsdeskundigen():
            onderzoek_id = request.args.get('onderzoek_id')
            user_id = g.current_user if g.current_user else None
            user = g.current_user if g.current_user else None

            if not onderzoek_id:
                return "Geen onderzoek_id meegegeven", 400

            if not user_id:
                return "Geen gebruiker ingelogd.", 401

            try:
                queries = self.get_queries()
                get_onderzoek = queries['get_onderzoek']

                user_id = user_id[0] if isinstance(user_id, tuple) else user_id
                onderzoeken = self.execute_query_one(get_onderzoek, (onderzoek_id,))
                deelnemende_onderzoeken = self.check_deelname(user_id)

                if not onderzoeken:
                    return "Onderzoek niet gevonden", 404
                print(f"{onderzoeken}")

                return render_template('info_onderzoek_ervaringsdeskundigen.html',
                                       onderzoeken=[onderzoeken],
                                       onderzoek_id=onderzoek_id,
                                       user_id=user_id,
                                       deelnemende_onderzoeken=deelnemende_onderzoeken,
                                       user=user,
                                       )

            except Exception as e:
                print(f"Fout tijdens het verwerken van de onderzoeken: {e}")
                return "Interne serverfout", 500

        @self._blueprint.route("/voorwaarden", methods=["GET", "POST"])
        def voorwaarden():
            return render_template('voorwaarden.html')

        @self._blueprint.route("/profiel_ervaringsdeskundigen", methods=["GET", "POST"])
        def profiel_ervaringsdeskundigen():
            user_id = g.current_user if g.current_user else None
            user = g.current_user if g.current_user else None

            if not user_id:
                return "Geen gebruiker ingelogd.", 401

            try:
                queries = self.get_queries()
                profiel = queries['profiel']

                user_id = user_id[0] if isinstance(user_id, tuple) else user_id
                profiel_gebruiker = self.execute_query(profiel, (user_id,))

                print(profiel_gebruiker)

                return render_template('profiel_ervaringsdeskundigen.html',
                                       user_id=user_id,
                                       profiel_gebruiker=profiel_gebruiker,
                                       user=user,
                                       )

            except Exception as e:
                print(f"Fout tijdens het verwerken van de onderzoeken: {e}")
                return "Interne serverfout", 500

        @self._blueprint.route("/wijzigen_gebruiker_ervaringsdeskundigen", methods=["GET", "POST"])
        def wijzigen_gebruiker_ervaringsdeskundigen():
            user_id = g.current_user if g.current_user else None
            user = g.current_user if g.current_user else None

            if not user_id:
                return "Geen gebruiker ingelogd.", 401

            try:
                queries = self.get_queries()
                profiel = queries['profiel']
                update = queries['update']

                user_id = user_id[0] if isinstance(user_id, tuple) else user_id
                profiel_gebruiker = self.execute_query(profiel, (user_id,))

                # Note: update_profiel isn't used in the original code, so I'm leaving it out
                # self.execute_query(update, (user_id,))

                return render_template('wijzigen_gebruiker_ervaringsdeskundigen.html',
                                       user_id=user_id,
                                       profiel_gebruiker=profiel_gebruiker,
                                       user=user,
                                       )

            except Exception as e:
                print(f"Fout tijdens het verwerken van de onderzoeken: {e}")
                return "Interne serverfout", 500

        @self._blueprint.route("/api_deelnemen_uitschrijven", methods=["POST", 'DELETE'])
        def api_inschrijven_uitschrijven():
            onderzoek_id = request.args.get('onderzoek_id')
            method = request.form.get('_method')
            user_id = g.current_user if g.current_user else None

            if not user_id:
                return "Geen gebruiker ingelogd.", 401

            try:
                queries = self.get_queries()
                inschrijven = queries['inschrijven']
                uitschrijven = queries['uitschrijven']
                check_user = queries['check_user']

                user_id = user_id[0] if isinstance(user_id, tuple) else user_id
                gebruiker = self.execute_query_one(check_user, (user_id,))
                naam_gebruiker = gebruiker[1] if gebruiker else "Gebruiker"

                if method == "DELETE":
                    self.execute_write_query(uitschrijven, (user_id, onderzoek_id))
                    return jsonify({"message": "Je bent nu uitgeschreven!"})
                else:
                    self.execute_write_query(inschrijven, (naam_gebruiker, user_id, onderzoek_id))
                    return jsonify({"message": "Je bent ingeschreven, het duurt 1 dag voor goedkeuring!"})

            except Exception as e:
                print(f"Fout tijdens het verwerken bij het inschrijven of uitschrijven: {e}")
                return "Interne serverfout", 500

        app.register_blueprint(self._blueprint)
        return self._blueprint