from flask import Blueprint, request, abort, Response, Request
from flasgger import swag_from
from controllers.controller import Controller
from models import APIModel
import json

class APIController(Controller):

    GET = "GET"
    POST = "POST"
    PATCH = "PATCH"
    DELETE = "DELETE"

    METHODS_RUD = [GET, PATCH, DELETE]
    METHODS_READ_ONLY = [GET]

    def __init__(self, cfg):
        super().__init__(cfg)
        self._model = APIModel()

    def add_routes(self, app):
        self._blueprint = Blueprint("api_blueprint", __name__, template_folder="../templates/api", url_prefix="/api")

        # We'll also need to implement filters in some way, 
        # and allowing users to specify offset since we'll, most likely,
        # have to limit the actual results obtained for large DB requests

        # Implemented offset and limit, no filters yet

        self._blueprint.route(self.__versionify("Ervaringsdeskundige/<id>/"), endpoint='ervaringsdeskundige', methods=self.METHODS_RUD)(self.ervaringsdeskundige)
        self._blueprint.route(self.__versionify("Ervaringsdeskundige/"), endpoint="ervaringsdeskundige", methods=[self.POST])(self.ervaringsdeskundige)
        self._blueprint.route(self.__versionify("Ervaringsdeskundigen/"), endpoint='ervaringsdeskundigen', methods=self.METHODS_READ_ONLY)(self.ervaringsdeskundigen)
        self._blueprint.route(self.__versionify("Onderzoek/<id>/"), endpoint='onderzoek', methods=self.METHODS_RUD)(self.onderzoek)
        self._blueprint.route(self.__versionify("Onderzoek/"), endpoint="onderzoek", methods=[self.POST])(self.onderzoek)
        self._blueprint.route(self.__versionify("Onderzoeken/"), endpoint='onderzoeken', methods=self.METHODS_READ_ONLY)(self.onderzoeken)

        app.register_blueprint(self._blueprint)
        return self._blueprint
    
    @swag_from('..\\docs\\ervaringsdeskundige\\ervaringsdeskundige_get.yml', endpoint='api_blueprint.ervaringsdeskundige', methods=[GET])
    @swag_from('..\\docs\\ervaringsdeskundige\\ervaringsdeskundige_post.yml', endpoint='api_blueprint.ervaringsdeskundige', methods=[POST])
    @swag_from('..\\docs\\ervaringsdeskundige\\ervaringsdeskundige_patch.yml', endpoint='api_blueprint.ervaringsdeskundige', methods=[PATCH])
    @swag_from('..\\docs\\ervaringsdeskundige\\ervaringsdeskundige_delete.yml', endpoint='api_blueprint.ervaringsdeskundige', methods=[DELETE])
    def ervaringsdeskundige(self, id:int=None):
        org_id = self._validate_request(request)
        if not org_id:
            return {'error': 'Er is geen valide api key meegegeven om dit verzoek te verwerken'}, 403
        match request.method:
            case self.GET:
                data = self.model.get_ervaringsdeskundige(id)
                if not data:
                    return {'error': 'Geen ervaringsdeskundige met dit id gevonden'}, 404
                return json.dumps(data), 200
            case self.POST:
                args = self.parse_request_data(request)
                if isinstance(data, Response): #If loading failed, a 415 error is returned, rethrow this
                    return args
                if args is None:
                    return {'error': 'Lege data terug gekregen uit verzoek'}, 415
                data = self.model.post_ervaringsdeskundige(args)
                if not isinstance(data, int):
                    return {'error': 'Het aanmaken van een ervaringsdeskundige is niet gelukt'}, 500
                return data, 200
            case self.PATCH:
                args = self.parse_request_data(request)
                if isinstance(data, Response): #If loading failed, a 415 error is returned, rethrow this
                    return args
                if args is None:
                    return {'error': 'Lege data terug gekregen uit verzoek'}, 415
                if id is None:
                    return {'error': 'Missend id in verzoek'}, 415
                data = self.model.patch_ervaringsdeskundige(id, args)
                return "", 200
            case self.DELETE:
                if id is None:
                    return {'error': 'Missend id in verzoek'}, 415
                data = self.model.delete_ervaringsdeskundige(id)
                return "", 200
            case _:
                return abort(405) #Throw unsupported method error

    @swag_from('..\\docs\\ervaringsdeskundige\\ervaringsdeskundigen_get.yml', endpoint='api_blueprint.ervaringsdeskundigen', methods=[GET])
    def ervaringsdeskundigen(self):
        if request.method != self.GET:
            return abort(405) #Throw unsupported method error
        org_id = self._validate_request(request)
        if not org_id:
            return {'error': 'Er is geen valide api key meegegeven om dit verzoek te verwerken'}, 403
        limit, offset = self.get_limit_offset_params(request)
        params = self.get_search_param_dict(request)
        data = self.model.get_ervaringsdeskundige(limit=limit, offset=offset, params=params)
        return json.dumps(data), 200
    
    @swag_from('..\\docs\\onderzoek\\onderzoek_get.yml', endpoint='api_blueprint.onderzoek', methods=[GET])
    @swag_from('..\\docs\\onderzoek\\onderzoek_post.yml', endpoint='api_blueprint.onderzoek', methods=[POST])
    @swag_from('..\\docs\\onderzoek\\onderzoek_patch.yml', endpoint='api_blueprint.onderzoek', methods=[PATCH])
    @swag_from('..\\docs\\onderzoek\\onderzoek_delete.yml', endpoint='api_blueprint.onderzoek', methods=[DELETE])
    def onderzoek(self, id:int=None):
        org_id = self._validate_request(request)
        if not org_id:
            return {'error': 'Er is geen valide api key meegegeven om dit verzoek te verwerken'}, 403
        match request.method:
            case self.GET:
                data = self.model.get_onderzoek(id, org_id)
                if not data:
                    return {'error': 'Geen onderzoek met dit id gevonden binnen uw organizatie'}, 404
                return json.dumps(data)
            case self.POST:
                args = self.parse_request_data(request)
                if isinstance(args, Response): #If loading failed, a 415 error is returned, rethrow this
                    return args
                if args is None:
                    return {'error': 'Lege data terug gekregen uit verzoek'}, 415
                data = self.model.post_onderzoek(org_id, args)
                if not isinstance(data, int):
                    return {'error': 'Het aanmaken van een onderzoek is niet gelukt'}, 500
                return json.dumps(data), 200
            case self.PATCH:
                args = self.parse_request_data(request)
                if isinstance(data, Response): #If loading failed, a 415 error is returned, rethrow this
                    return args
                if args is None:
                    return {'error': 'Lege data terug gekregen uit verzoek'}, 415
                if id is None:
                    return {'error': 'Missend id in verzoek'}, 415
                data = self.model.patch_onderzoek(id, org_id, args)
                return "", 200
            case self.DELETE:
                if id is None:
                    return {'error': 'Missend id in verzoek'}, 415
                data = self.model.delete_onderzoek(id, org_id)
                return "", 200
            case _:
                return abort(405) #Throw unsupported method error

    @swag_from('..\\docs\\onderzoek\\onderzoeken_get.yml', endpoint='api_blueprint.onderzoeken', methods=[GET])
    def onderzoeken(self):
        if request.method != self.GET:
            return abort(405) #Throw unsupported method error
        org_id = self._validate_request(request)
        if not org_id:
            return {'error': 'Er is geen valide api key meegegeven om dit verzoek te verwerken'}, 403
        limit, offset = self.get_limit_offset_params(request)
        data = self.model.get_onderzoek(org_id=org_id, limit=limit, offset=offset)
        if not data:
            return {'error': 'Geen onderzoek gevonden binnen uw organizatie die voldoen aan opgegeven criteria'}, 404
        for i in range(len(data)):
            data[i] = dict(data[i])
        return json.dumps(data), 200
    
    def parse_request_data(self, request)->Response|dict|None:
        if not request.is_json:
            return abort(415) #Throw unsupported media error
        data = request.get_json()
        #Add instance check for list for multi-item post?
        return data
    
    def get_limit_offset_params(self, request):
        limit = request.args.get('limit', type=int)
        offset = request.args.get('offset', type=int)
        if limit is None or limit <= 0:
            limit = 20
        if offset is None or offset < 0:
            offset = 0
        return limit, offset
    
    def get_search_param_dict(self, request):
        return dict([(key, request.args[key]) for key in request.args.keys() if key != 'limit' and key != 'offset'])
    
    def _validate_request(self, request: Request):
        if True:
            return 1
        api_key = request.headers.get('Authorization')
        org = self.model.get_org_from_key(api_key)
        if org is None:
            return False
        return org['id']

    def __versionify(self, route:str, version:float=1):
        return f'/v{version}/{route}'