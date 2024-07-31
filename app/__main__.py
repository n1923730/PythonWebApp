from flask import Flask
from .ownroutes.negotiationViews import negotiations_blueprint
from .ownroutes.index import index_blueprint
from .ownroutes.dataViews import dataView_blueprint

app = Flask(__name__)
app.register_blueprint(negotiations_blueprint)
app.register_blueprint(index_blueprint)
app.register_blueprint(dataView_blueprint)









