from flask import Flask
from flask_restful import Resource, Api
import os
import json

app = Flask(__name__)
api = Api(app)

tablo = {}

def init(table):
    path = "./images"
    file_list = os.listdir(path)
    absp = os.getcwd() #chemin du répertoire de travail
    for i in range (0,len(file_list)):
        table.update({i:file_list[i]})


init(tablo)
print(tablo)

class lectureImg(Resource):
    
    def get(self):
        return tablo

    def post(self):
        pass

    def delete(self):
        pass

api.add_resource(lectureImg, '/images')

if __name__ == '__main__':
    app.run(debug=True)
