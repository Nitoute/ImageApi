from flask import Flask
from flask_restful import Resource, Api, reqparse
import os
from flask import send_file
import werkzeug

app = Flask(__name__)
api = Api(app)

tablo = {}
path = "./images"


def refaireTab(table, client_nom):
    tablo.clear()
    path_dir = path + "/" + client_nom
    file_list = os.listdir(path_dir)
    for i in range(0, len(file_list)):
        table.update({i + 1: file_list[i]})


def init(table):
    index = 0
    file_list = os.listdir(path)
    for i in file_list:

        path_dir = path + "/" + i
        file_list2 = os.listdir(path_dir)

        for j in file_list2:
            index += 1
        table.update({i: index})
        index = 0
    


class initLectureImg(Resource):

    def get(self):

        tablo.clear()
        init(tablo)
        return tablo


class lectureImg(Resource):

    def get(self, client_nom):
        
        tablo.clear()
        refaireTab(tablo, client_nom)
        return tablo


class ImageListApi(Resource):

    def delete(self, client_nom, img_id):
        print(img_id)
        refaireTab(tablo, client_nom)
        print("ancien tableau :", tablo)
        imgASuprim = tablo[int(img_id)]
        print("img à supprimé :", imgASuprim)
        tablo.pop(int(img_id), None)
        os.remove(path + '/' + client_nom + '/' + imgASuprim)
        tablo.clear()
        refaireTab(tablo, client_nom)
        print("nouveau tableau :", tablo)
        return tablo

    def get(self, client_nom, img_id):
        refaireTab(tablo, client_nom)
        imgAEnvoi = path + '/' + client_nom + '/' + tablo[int(img_id)]
        return send_file(imgAEnvoi, mimetype='image/gif')

    def post(self, client_nom, img_id):
        refaireTab(tablo, client_nom)
        tablValu = tablo.values()
        if (img_id in tablValu):
            print("fichier déja existant")
            return tablo
        else:
            print("le fichier n'existe pas je l'ajoute !")
            parse = reqparse.RequestParser()
            parse.add_argument('file',
                               type=werkzeug.datastructures.FileStorage,
                               location="files")
            args = parse.parse_args()
            imgFile = args['file']
            imgFile.save(os.path.join("images/" + client_nom, img_id))
            tablo.update({len(tablo) + 1: img_id})
            print("tablo retourné :", tablo)
            return tablo


api.add_resource(initLectureImg, '/images')
api.add_resource(lectureImg, '/images/<client_nom>')
api.add_resource(ImageListApi, '/ImageListApi/<client_nom>/<img_id>')


if __name__ == '__main__':
    app.run(debug=True)
