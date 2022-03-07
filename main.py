from flask import Flask
from flask_restful import Resource, Api, reqparse
import os
from flask import send_file
import werkzeug

app = Flask(__name__)
api = Api(app)

tablo = {}
path = "./images"

# prend 2 arguments: un tableau(tableau courant), un client nom (le client en cours de traitement)
# fonction qui réécrit le tableau en fonction du nom du client (affiche la page du client)
def refaireTab(table, client_nom):
    tablo.clear()
    path_dir = path + "/" + client_nom
    file_list = os.listdir(path_dir)
    for i in range(0, len(file_list)):
        table.update({i + 1: file_list[i]})


# prend 1 argument: un tableau(tableau courant)
# fonction qui permet d'afficher la page d'acceuil
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
    

#get qui permet au clique de l'utilisateur sur Clients de retourner à la page d'acceuil
class initLectureImg(Resource):

    def get(self):

        tablo.clear()
        init(tablo)
        return tablo

# prend 1 argument: le nom du client(le client voulu)
#get qui permet au clique de l'utilisateur sur un des pseudos des clients de retourner la page du client
class lectureImg(Resource):

    def get(self, client_nom):
        
        tablo.clear()
        refaireTab(tablo, client_nom)
        return tablo



# prend 2 arguments: le nom du client(le client voulu), l'image id (index de l'image à traiter)
#delete qui permet au clique de l'utilisateur sur l'icone poubelle d'une image de supprimer l'image
#get qui permet au clique de l'utilisateur un nom d'image d'obtenir une prévisualisation de l'image
#post qui permet de récupérer une image d'un utilisateur pour la mettre dans le repertoire du client
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
