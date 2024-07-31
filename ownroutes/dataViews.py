from flask import render_template, Blueprint, g
from .negotiationViews import Negotiation
import json
import matplotlib.pyplot as plt
import matplotlib.dates as dates
from datetime import datetime 


dataView_blueprint = Blueprint("dataView", __name__, url_prefix="/negotiations/dataview")

class DataView:

    @dataView_blueprint.route('/')
    def dataView():
        data = Negotiation.requestData()
        data_json = json.loads(data)

        id_array = []
        value_array = []
        timestamp_array = []
        for array in data_json:
            id_array.append(array['id'])
            value_array.append(int(array['value']))
            dt = datetime.strptime(array['timestamp'], '%Y-%m-%d %H:%M:%S')
            t = dt.time()
            print(t)
            timestamp_array.append(str(t))


        fig, ax = plt.subplots()

        ax.plot(timestamp_array, value_array)

        plt.xlabel('Zeit')
        plt.ylabel('Füllstand')

        plt.title('Entwicklung des Füllstandes')

        plt.gcf().autofmt_xdate()

        plt.yticks([10,20,30,40,50])
        plt.xticks (timestamp_array, rotation='vertical')

        plt.savefig('./templates/plot.png')  
        
        return render_template('dataView.html', len = len(data_json), data = data_json)   
    

