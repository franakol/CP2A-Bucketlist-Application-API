from flask import Flask
from flask_restx import Api
from .bucketlists.views import bucketlist_namespace
from .auth.views import auth_namespace
from .config.config import config_dict
from .utils import db
from .models.bucketlists import Bucketlist
from .models.users import User
from .models.items import Item
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from .models import Base
from flask_cors import CORS
from werkzeug.exceptions import NotFound, MethodNotAllowed


def create_app(config=config_dict['dev']):
    app=Flask(__name__)
    app.config.from_object(config)

    
    

    authorizations={
        "Bearer Auth":{
            'type':"apiKey",
            'in':'header',
            'name':"Authorization",
            'description':"Add a JWT with ** Bearer &lt;JWT&gt; to authorize"
        }
    }
    cors = CORS(app, resources={r"*": {"origins": "*"}})
    
    api=Api(app,
        title="CP2A - BucketList Application API",
        description="REST API for a Bucketlist Application using flask",
        authorizations=authorizations,
        security="Bearer Auth"

    )
    

    api.add_namespace(bucketlist_namespace,path='/bucketlists')
    api.add_namespace(auth_namespace,path='/auth')
    

    
    db.init_app(app)

    jwt=JWTManager(app)
    
    migrate=Migrate(app,db)

    @api.errorhandler(NotFound)
    def not_found(error):
        return{"error":"Not Found"},404

    @api.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return{"error": "Method Not Allowed"},405



    
    @app.shell_context_processor
    def make_shell_context():
        return{
            'db':db,
            'User':User,
            'Bucketlist':Bucketlist,
            'Item':Item
        }

    return app