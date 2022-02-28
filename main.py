from flask import Flask
from flask_restful import Resource, Api
import os
import json

app = Flask(__name__)
api = Api(app)

tablo = {}

class lectureImg(Resource):
    print("test")
    path = "./images"
    file_list = os.listdir(path)
    absp = os.getcwd() #chemin du répertoire de travail
    print(file_list)
    
    for i in range (0,len(file_list)):
        tablo.update({i:file_list[i]})
    
    def get(self):
        return tablo

api.add_resource(lectureImg, '/images')

if __name__ == '__main__':
    app.run(debug=True)
