from flask import render_template, Blueprint
from flask import request, redirect
from .negotiationViews import Negotiation

index_blueprint = Blueprint("index", __name__)


class Index:

    @index_blueprint.route('/', methods=['POST', 'GET'])
    def start():
        if request.method == 'GET':
            return render_template('index.html')
        if request.method == 'POST':
            ProducerIp = request.form['ProdIP']
            print(ProducerIp)
            Negotiation.registerProducerIp(ProducerIp)
            return redirect('http://127.0.0.1:5000/negotiations')



    @index_blueprint.route('/index', methods=['Get'])
    def getIndex():
        return render_template('index.html')






