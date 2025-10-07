from models.model import Model
import bleach

class APIModel(Model):

    ALLOWED_TAGS = ['b', 'i', 'u', 'a']
    
    def get_ervaringsdeskundige(self, id:int=None, limit:int=20, offset:int=0, params:dict[str, str] = {}):
        ervaringsdeskundigen = None
        if id is None:
            clause = self._build_where_clause('ervaringsdeskundige', params)
            ervaringsdeskundigen = self.query(f"SELECT * FROM ervaringsdeskundigen {clause} LIMIT ?, ?", offset, limit)
            if ervaringsdeskundigen is None:
                return None
            status_list = {item['id']: dict(item) for item in self.query("SELECT * FROM status")}
            beperking_categorie_list = {item['id']: dict(item) for item in self.query("SELECT * FROM beperkingcategorie")}
            output = []
            for ervaringsdeskundige in ervaringsdeskundigen:
                data = self._map_output(ervaringsdeskundige, 'ervaringsdeskundige')
                data['status'] = status_list.get(ervaringsdeskundige['status_id'])
                data['toezichthouder'] = dict(self.query("SELECT * FROM toezichthouders WHERE id=?", ervaringsdeskundige['toezichthouder_id']))
                beperkingen = self.query("SELECT beperkingen.* FROM ervaringsdeskundigen_beperkingen INNER JOIN beperkingen ON beperkingen.id=beperking_id WHERE ervaringsdeskundige_id=?", ervaringsdeskundige['id'])
                data['beperkingen'] = []
                for beperking in beperkingen:
                    bdata = {'id': beperking['id'], 'naam': beperking['naam']}
                    bdata['categorie'] = beperking_categorie_list.get(beperking['categorie_id'])
                    data['beperkingen'].append(bdata)
                output.append(data)
            return output
        
        ervaringsdeskundigen = self.query("SELECT * FROM ervaringsdeskundigen WHERE id=?", id, first=True)
        if ervaringsdeskundigen is None:
            return None
        status_list = {item['id']: dict(item) for item in self.query("SELECT * FROM status")}
        beperking_categorie_list = {item['id']: dict(item) for item in self.query("SELECT * FROM beperkingcategorie")}
        data = self._map_output(ervaringsdeskundigen, 'ervaringsdeskundige')
        data['status'] = status_list.get(ervaringsdeskundigen['status_id'])
        data['toezichthouder'] = dict(self.query("SELECT * FROM toezichthouders WHERE id=?", ervaringsdeskundigen['toezichthouder_id']))
        beperkingen = self.query("SELECT beperkingen.* FROM ervaringsdeskundigen_beperkingen INNER JOIN beperkingen ON beperkingen.id=beperking_id WHERE ervaringsdeskundige_id=?", ervaringsdeskundigen['id'])
        data['beperkingen'] = []
        for beperking in beperkingen:
            bdata = {'id': beperking['id'], 'naam': beperking['naam']}
            bdata['categorie'] = beperking_categorie_list.get(beperking['categorie_id'])
            data['beperkingen'].append(bdata)
        return data
    
    def post_ervaringsdeskundige(self, data:dict[str, str]):
        if not self._has_all_keys(data.keys(), [key for key in self.KEY_MAP['ervaringsdeskundige'].keys() if self.KEY_MAP['ervaringsdeskundige'][key][0]]):
            return {"error": "Not all required keys included in data"}
        query_str = self._create_insert_statement_for('ervaringsdeskundigen', data)
        return self.query(query_str, *data.values(), id=True)

    def patch_ervaringsdeskundige(self, id, data):
        query_str = self._create_update_statement_for('ervaringsdeskundigen', id, data)
        items = list(data.values)
        items.append(id)
        return self.query(query_str, *items)

    def delete_ervaringsdeskundige(self, id):
        return self.query("DELETE FROM ervaringsdeskundigen WHERE id=?", id)
    
    def get_onderzoek(self, id:int=None, org_id:int=None, limit:int=20, offset:int=0):
        organisaties = None
        if id is None:
            clause = self._build_where_clause('onderzoek', params)
            organisaties = self.query(f"SELECT * FROM onderzoeken {clause} AND organisatie_id=? LIMIT ?, ?", org_id, offset, limit)
            if not organisaties:
                return None
            status_list = {item['id']: dict(item) for item in self.query("SELECT * FROM status")}
            beperking_categorie_list = {item['id']: dict(item) for item in self.query("SELECT * FROM beperkingcategorie")}
            output = []
            for onderzoek in onderzoeken:
                data = self._map_output(onderzoek, 'onderzoek')
                data['status'] = status_list.get(onderzoek['status_id'])
                beperkingen = self.query("SELECT beperkingen.* FROM onderzoek_beperkingen INNER JOIN beperkingen ON beperkingen.id=beperking_id WHERE onderzoek_id=?", onderzoek['id'])
                data['beperkingen'] = []
                for beperking in beperkingen:
                    bdata = {'id': beperking['id'], 'naam': beperking['naam']}
                    bdata['categorie'] = beperking_categorie_list.get(beperking['categorie_id'])
                    data['beperkingen'].append(bdata)
                output.append(data)
            return output
        organisaties = self.query("SELECT * FROM onderzoeken WHERE id=? AND organisatie_id=?", id, org_id, first=True)
        if not organisaties:
            return None
        status_list = {item['id']: dict(item) for item in self.query("SELECT * FROM status")}
        beperking_categorie_list = {item['id']: dict(item) for item in self.query("SELECT * FROM beperkingcategorie")}
        data = self._map_output(onderzoek, 'onderzoek')
        data['status'] = status_list.get(onderzoek['status_id'])
        beperkingen = self.query("SELECT beperkingen.* FROM onderzoek_beperkingen INNER JOIN beperkingen ON beperkingen.id=beperking_id WHERE onderzoek_id=?", onderzoek['id'])
        data['beperkingen'] = []
        for beperking in beperkingen:
            bdata = {'id': beperking['id'], 'naam': beperking['naam']}
            bdata['categorie'] = beperking_categorie_list.get(beperking['categorie_id'])
            data['beperkingen'].append(bdata)
        return data
    
    def post_onderzoek(self, org_id, data):
        data['organisatie_id'] = org_id
        if not self._has_all_keys(data.keys(), [key for key in self.KEY_MAP['onderzoek'].keys() if self.KEY_MAP['onderzoek'][key][0]]):
            return {"error": "Not all required keys included in data"}
        query_str = self._create_insert_statement_for('onderzoeken', data)
        return self.query(query_str, *data.values(), id=True)

    def patch_onderzoek(self, id, org_id, data):
        query_str = self._create_update_statement_for('onderzoeken', data)
        items = list(data.values)
        items.append(id)
        items.append(org_id)
        return self.query(query_str, *items)

    def delete_onderzoek(self, id, org_id):
        return self.query("DELETE FROM onderzoeken WHERE id=? AND organisatie_id=?", id, org_id)
    
    def get_org_from_key(self, api_key:str):
        if not api_key:
            return None
        return self.query("SELECT * FROM organisaties WHERE api_key=?", api_key, first=True)

    def _create_insert_statement_for(self, table:str, data:dict[str, str]):
        query_str = "INSERT INTO " + table + " ("
        for key in data.keys():
            query_str += key + ','
        query_str = query_str.strip(', ')
        query_str += ") VALUES ("
        for key in data.keys():
            query_str += '?,'
        query_str = query_str.strip(', ')
        query_str += ");"
        return query_str

    def _create_update_statement_for(self, table:str, data:dict[str, str]):
        query_str = "UPDATE " + table + " SET "
        for key in data.keys():
            query_str += key + "=" + '?, '
        query_str = query_str.strip(', ')
        query_str += " WHERE id=? AND organisatie_id=?;"
        return query_str

    def _has_all_keys(self, keys:list, required:list):
        for key in required:
            if not key in keys:
                return False
        return True
    
    def _search_param_to_where_clause(self, target:str, key:str, value_format:str):
        if not key in self.KEY_MAP[target]:
            return ''
        value = self._parse_value_format(value_format)
        return key + value

    def _parse_value_format(self, value_format:str):
        if not value_format:
            return ' IS NOT NULL'
        
        value_format = value_format.strip('\'\"')
        value_format = bleach.clean(value_format, self.ALLOWED_TAGS, strip=True) #Sanitize all query params

        if '?' in value_format or '*' in value_format:
            return ' LIKE \'' + value_format.replace('?', '%').replace('*', '%') + '\''
        
        if value_format.startswith('(') and value_format.endswith(')'):
            return ' IN ' + value_format

        return '=\'' + value_format + '\''
    
    def _build_where_clause(self, target:str, params:dict[str, str]):
        if len(params) <= 0:
            return ''
        clause = "WHERE "
        for key in params.keys():
            q = self._search_param_to_where_clause(target, key, params[key])
            if not q:
                continue
            clause += q
            clause += ' AND '
        clause = clause.removesuffix(' AND ')
        return clause
    
    def _map_output(self, row, target):
        data = {}
        for key in row.keys():
            if not self.KEY_MAP[target][key][1]:
                continue
            data[key] = row[key]
        return data

    # Map the keys for all tables with api-routes value for each key is: tuple(Required for input?, Include in output?)
    KEY_MAP = {
        'ervaringsdeskundige': {
            'id': (False, True),
            'voornaam': (True, True),
            'achternaam': (True, True),
            'postcode': (True, True),
            'geslacht': (True, True),
            'telefoonnr': (True, True),
            'email': (True, True),
            'wachtwoord': (True, False),
            'salt': (True, False),
            'geboorte_datum': (True, True),
            'gebruikte_hulpmiddelen': (False, True),
            'kort_voorstellen': (False, True),
            'bijzonderheden': (False, True),
            'toezichthouder_id': (False, False),
            'voorkeur_benadering': (False, True),
            'type_onderzoek': (False, True),
            'bijzonderheden_beschikbaarheid': (False, True),
            'voorwaarden': (False, True),
            'status_id': (False, False)
        },
        'onderzoek': {
            'id': (False, True),
            'titel': (True, True),
            'status_id': (False, False),
            'beschikbaar': (True, True),
            'beschrijving': (True, True),
            'start_datum': (True, True),
            'eind_datum': (True, True),
            'type_onderzoek': (True, True),
            'locatie': (False, True),
            'met_beloning': (False, True),
            'beloning': (True, True),
            'doelgroep_leeftijd_start': (True, True),
            'doelgroep_leeftijd_eind': (True, True),
            'organisatie_id': (True, False)
        }
    }
