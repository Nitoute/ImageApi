from logging import raiseExceptions
from flask import Flask,request
from flask_restful import Resource, Api, reqparse
import os
import json
from flask import send_file
import werkzeug

app = Flask(__name__)
api = Api(app)

tablo = {}
path = "./images"
def init(table):
    file_list = os.listdir(path)
    absp = os.getcwd() #chemin du répertoire de travail
    for i in range (0,len(file_list)):
        table.update({i+1:file_list[i]})
    

init(tablo)
print(tablo)

class lectureImg(Resource):
    
    def get(self):
        print("tabloget",tablo)
        return tablo



class supprimerImg(Resource):

    def delete(self,img_id):
        print(img_id)
        print("ancien tableau :",tablo)
        imgASuprim=tablo[int(img_id)]
        print("img à supprimé :",imgASuprim)
        tablo.pop(int(img_id),None)
        os.remove(path+'/'+imgASuprim)
        tablo.clear()
        init(tablo)
        print("nouveau tableau :",tablo)
        return tablo
    

class imgAfficher(Resource):
    def get(self,img_id):
        
        imgAEnvoi=path+'/'+tablo[int(img_id)]
        return send_file(imgAEnvoi, mimetype='image/gif')

    
class AddImg(Resource):
    def post(self,img_nom):
        tablValu = tablo.values()
        if (img_nom in tablValu) :
            print("fichier déja existant")
            return -1
        else :
            print("le fichier n'existe pas je l'ajoute !")
            parse = reqparse.RequestParser()
            parse.add_argument('file', type=werkzeug.datastructures.FileStorage,location="files")
            args = parse.parse_args()
            imgFile = args['file']
            imgFile.save(os.path.join("images/",img_nom))
            tablo.update({len(tablo):img_nom})
            print("tablo retourné :",tablo)
            return tablo

api.add_resource(lectureImg, '/images')
api.add_resource(supprimerImg, '/images/<img_id>')
api.add_resource(AddImg, '/imagesUpload/<img_nom>')
api.add_resource(imgAfficher, '/imagesAfficher/<img_id>')

if __name__ == '__main__':
    app.run(debug=True)
