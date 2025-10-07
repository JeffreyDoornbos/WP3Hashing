# from flask import Flask, request, render_template, redirect, url_for, jsonify
# from urllib.parse import urlencode
# import sqlite3
# import os
#
# app = Flask(__name__, template_folder=os.path.join("static/aanvragen_pagina(ervaringsdeskundigen)", "templates"))
#
# DATABASE_FILE = "database/database.db"
#
# def load_queries(path):
#     queries = {}
#     query_name = None
#     parameters = []
#
#     with open(path, 'r') as file:
#         for line in file:
#             line = line.strip()
#             print(f"Processing line: {line}")
#             if line.startswith('-- [') and line.endswith(']'):
#                 if query_name and parameters:
#                     queries[query_name] = ' '.join(parameters).rstrip(';')
#                 query_name = line[4:-1]
#                 parameters = []
#             elif query_name:
#                 if line:
#                     parameters.append(line)
#
#         if query_name and parameters:
#             queries[query_name] = ' '.join(parameters).rstrip(';')
#
#     return queries
#
# @app.route("/")
# def home_redirect():
#     return redirect(url_for('lopende_onderzoeken_ervaringsdeskundigen'))
#
# @app.route('/process', methods=['POST'])
# def process():
#
#   try:
#     print("Ontvangen data:", request.form)
#
#     lijst = [
#         "voornaam", "achternaam", "postcode", "geslacht",
#         "email", "telefoonnummer", "geboortedatum", "type_beperking",
#         "akkoord_voorwaarden", "toezichthouder", "naam_voogd_toezichthouder",
#         "e_mailadres_voogd_toezichthouder", "telefoonnummer_voogd_toezichthouder",
#         "voorkeur_benadering", "type_onderzoek", "bijzonderheden_beschikbaarheid",
#     ]
#
#     ontbrekende_namen = [naam for naam in lijst if not request.form.get(naam)]
#
#     if ontbrekende_namen:
#         return jsonify({'error': f'Vul de volgende verplichte velden in: {", ".join(ontbrekende_namen)}'})
#
#     return jsonify({'message': 'Formulier succesvol verzonden!'})
#
#   except Exception as e:
#       return jsonify({'error': str(e)})
#
# @app.route("/nieuwe_gebruiker_ervaringsdeskundigen", methods=["GET","POST"])
# def nieuwe_gebruiker_ervaringsdeskundigen():
#         return render_template(
#             'src/templates/aanvragen_pagina(ervaringsdeskundigen)/nieuwe_gebruiker_ervaringsdeskundigen.html')
#
#
# @app.route("/lopende_onderzoeken_ervaringsdeskundigen", methods=["GET","POST"])
# def lopende_onderzoeken_ervaringsdeskundigen():
#     try:
#         conn = sqlite3.connect('database/database.db')
#         cursor = conn.cursor()
#
#         queries = load_queries('database/queries/queries.sql')
#
#         normal_query = queries['normal_query']
#         count_query = queries['count_query']
#         doelgroep_query = queries['doelgroep_query']
#         # beschikbaar_query = queries['beschikbaar_query']
#
#         # zoeken in de onderzoeken
#         search = request.args.get("search", '').strip()
#         doelgroep = request.args.get("doelgroep", '').strip()
#         beschikbaar = request.args.get("beschikbaar", '').strip()
#
#         # Dit is voor de pagina nummers
#         page = int(request.args.get('page', 1))
#         per_page = 10
#         start = (page - 1) * per_page
#
#         query = normal_query.replace("SELECT", "SELECT onderzoeken.id, ")
#         parameters = []
#
#         if search:
#             query += " HAVING onderzoeken.titel LIKE ?"
#             parameters.append(f"%{search}%")
#
#         if doelgroep:
#             query += " HAVING GROUP_CONCAT(beperkingen.naam, ', ') LIKE ?"
#             parameters.append(f"%{doelgroep}%")
#
#         if beschikbaar:
#             query += " HAVING onderzoeken.beschikbaar IS NOT 0 OR NULL"
#
#         query += " LIMIT ? OFFSET ?"
#         parameters.extend([per_page, start])
#
#         cursor.execute(query, parameters)
#         onderzoeken = cursor.fetchall()
#
#         count_parameters = []
#
#         if search:
#             count_query += " AND onderzoeken.titel LIKE ?"
#             count_parameters.append(f"%{search}%")
#
#         if count_parameters:
#             cursor.execute(count_query, count_parameters)
#         else:
#             cursor.execute(count_query)
#
#         totale_onderzoeken = cursor.fetchone()[0]
#
#         total_pages = (totale_onderzoeken + per_page - 1) // per_page
#         next_page = page + 1 if page < total_pages else None
#         prev_page = page - 1 if page > 1 else None
#
#         show_first = page > 1
#         show_last = page < total_pages
#
#         base_params = {
#             "search": search,
#             "doelgroep": doelgroep,
#             "beschikbaar": beschikbaar,
#         }
#
#         page_numbers = []
#         for i in range(1, total_pages + 1):
#             base_params["page"] = i
#             page_numbers.append(f"?{urlencode(base_params)}")
#
#         cursor.execute(doelgroep_query)
#         doelgroepen = [row[1] for row in cursor.fetchall()]
#
#         return render_template(
#             'src/templates/aanvragen_pagina(ervaringsdeskundigen)/lopende_onderzoeken_ervaringsdeskundigen.html',
#             onderzoeken=onderzoeken,
#             page=page,
#             next_page=next_page,
#             prev_page=prev_page,
#             total_pages=total_pages,
#             page_numbers=page_numbers,
#             show_first=show_first,
#             show_last=show_last,
#             search=search,
#             doelgroep=doelgroep,
#             beschikbaar=beschikbaar,
#             doelgroepen=doelgroepen)
#
#     except Exception as e:
#         print(f"Fout tijdens het verwerken van de lopende onderzoeken: {e}")
#         return "Interne serverfout", 500
#     finally:
#         conn.close()
#
# @app.route("/voorwaarden", methods=["GET","POST"])
# def voorwaarden():
#         return render_template('src/templates/aanvragen_pagina(ervaringsdeskundigen)/voorwaarden.html')
#
# @app.route("/wijzigen_gebruiker_ervaringsdeskundigen", methods=["GET","POST"])
# def wijzigen_gebruiker_ervaringsdeskundigen():
#         return render_template(
#             'src/templates/aanvragen_pagina(ervaringsdeskundigen)/wijzigen_gebruiker_ervaringsdeskundigen.html')
#
# @app.route("/deelnames_ervaringsdeskundigen", methods=["GET","POST"])
# def deelnames_ervaringsdeskundigen():
#         return render_template(
#             'src/templates/aanvragen_pagina(ervaringsdeskundigen)/deelnames_ervaringsdeskundigen.html')
#
# @app.route("/mailbox_ervaringsdeskundigen", methods=["GET","POST"])
# def mailbox_ervaringsdeskundigen():
#         return render_template('src/templates/aanvragen_pagina(ervaringsdeskundigen)/mailbox_ervaringsdeskundigen.html')
#
# if __name__ == '__main__':
#     app.run(debug=True)
