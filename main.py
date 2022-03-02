from flask import Flask,request
from flask_restful import Resource, Api
import os
import json

app = Flask(__name__)
api = Api(app)

tablo = {}
path = "./images"

def init(table):
    file_list = os.listdir(path)
    absp = os.getcwd() #chemin du répertoire de travail
    for i in range (0,len(file_list)):
        table.update({i:file_list[i]})


init(tablo)
print(tablo)

class lectureImg(Resource):
    
    def get(self):
        return tablo



class supprimerImg(Resource):

    def delete(self,img_id):
        print(img_id)
        print("ancien tableau :",tablo)
        imgASuprim=tablo[int(img_id)]
        print("img à supprimé :",imgASuprim)
        tablo.pop(int(img_id),None)
        os.remove(path+'/'+imgASuprim)
        print("nouveau tableau :",tablo)
        return tablo

class AddImg(Resource):
    def post(self,data):

        pass

api.add_resource(lectureImg, '/images')
api.add_resource(supprimerImg, '/images/<img_id>')
api.add_resource(AddImg, '/imagesUpload/<data>')
if __name__ == '__main__':
    app.run(debug=True)
