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

class supprimerImg(Resource):

    def delete(self,img_id):
        print(img_id)
        print("ancien tableau :",tablo)
        imgASuprim=tablo[int(img_id)]
        print("img à supprimé :",imgASuprim)
        tablo.pop(int(img_id),None)
        print("nouveau tableau :",tablo)
        return tablo

api.add_resource(lectureImg, '/images')
api.add_resource(supprimerImg, '/images/<img_id>')

if __name__ == '__main__':
    app.run(debug=True)
