from flask import Blueprint, send_file, render_template, jsonify
from controllers.controller import Controller
from models.home_model import OrganizationModel 

class HomeController(Controller):
    def add_routes(self, app):
        self._blueprint = Blueprint("home_blueprint", __name__, template_folder="../templates/home")

        self._blueprint.route('/apidefinitions/', methods=["GET"])(self.apidefinitions)
        self._blueprint.route('/', methods=["GET"])(self.homepage)
        self._blueprint.route('/api/organisaties_count', methods=["GET"])(self.organisaties_count)
        
        app.register_blueprint(self._blueprint)
        return self._blueprint
    
    def apidefinitions(self):
        return send_file('./docs/definitions.yml', mimetype='text/plain')
    
    def homepage(self):
        return render_template("homepage.html")
    
    def organisaties_count(self):
        org_count = OrganizationModel().get_organisaties_count()
        return jsonify({"count": org_count})