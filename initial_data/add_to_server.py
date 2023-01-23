import pathlib

import requests
from fastapi import File, UploadFile

# BASE_URL = "https://trena.gsi.mpmg.mp.br/f05_backend/"
BASE_URL = "http://0.0.0.0:8000/"

API_KEY = "0a944fb8-2bbc-4f03-a81a-bf84899cd4f2"

USER_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Imdlb3JnZUB0ZXN0ZS5jb20iLCJyb2xlIjoiQURNSU4iLCJleHAiOjE2Njg1MjA1NTl9.TQC-Drv_pCrDpyDGn-4QQdoSu7tdTckaqK8CosIHdr4"

NOTIFICATIONS_ID = []

def send(base_url, to_send):
    return requests.post(base_url,
                         headers={'X-TRENA-KEY': API_KEY, "token": USER_TOKEN},
                         json=to_send,
                         verify=False)


def add_municipios(uf_code: str):
    with open("cities/municipios.csv", "r") as f_in:
        lines = f_in.readlines()
        uploaded = 0
        municipios_sent = []
        for line in lines[1:]:
            municipio = line.strip().split(",")
            if municipio[5] == uf_code:
                municipios_sent.append({"codigo_ibge": municipio[0],
                                        "name": municipio[1],
                                        "latitude": municipio[2],
                                        "longitude": municipio[3],
                                        "uf": "MG"})
        response = send(BASE_URL + "address/city/addAll", municipios_sent)
        if response.status_code == 200:
            uploaded = len(municipios_sent)
        print("Municípios enviados: {0}".format(uploaded))


def add_type_works():
    with open("type_works/tipo_de_obras.csv", "r") as f_in:
        lines = f_in.readlines()
        uploaded = 0
        for line in lines[1:]:
            type_work = line.strip().split(",")
            response = send(BASE_URL + "typeworks/add",
                            {"flag": type_work[0],
                             "name": type_work[1],
                             "status_list": []
                             })
            if response.status_code == 200:
                uploaded = uploaded + 1
        print("Tipos de obras adicionadas: {0}".format(uploaded))


def add_type_works_work_statuses():
    with open("type_works/tipo_de_obras.csv", "r") as f_in:
        lines = f_in.readlines()
        uploaded = 0
        for line in lines[1:]:
            type_work = line.strip().split(",")
            response = send(BASE_URL + "typeworks/workStatus/update",
                            {"type_work_id": type_work[0],
                             "work_statuses": list(map(int, type_work[2].split('-')))
                             })
            if response.status_code == 200:
                uploaded = uploaded + 1
        print("Relações criadas: Tipos de obras - Estados das obras: {0}".format(uploaded))


def add_type_photos():
    with open("type_photos/tipo_de_fotos.csv", "r") as f_in:
        lines = f_in.readlines()
        uploaded = 0
        for line in lines[1:]:
            type_photo = line.strip().split(",")
            response = send(BASE_URL + "typephotos/add",
                            {"flag": type_photo[0],
                             "name": type_photo[1],
                             "description": type_photo[2]})
            if response.status_code == 200:
                uploaded = uploaded + 1
        print("Tipos de fotos adicionadas: {0}".format(uploaded))


def add_public_work():
    with open("public_work/obras.csv", "r") as f_in:
        lines = f_in.readlines()
        uploaded = 0
        for line in lines[1:]:
            public_work = line.strip().split(",")
            response = send(BASE_URL + "publicworks/add",
                            {
                                "id": public_work[0],
                                "name": public_work[1],
                                "type_work_flag": public_work[2],
                                "queue_status": public_work[3],
                                "queue_status_date": public_work[4],
                                "address": {
                                    "id": public_work[5],
                                    "street": public_work[6],
                                    "neighborhood": public_work[7],
                                    "number": public_work[8],
                                    "latitude": public_work[9],
                                    "longitude": public_work[10],
                                    "city": public_work[11],
                                    "state": public_work[12],
                                    "cep": public_work[13],
                                }
                            })
            if response.status_code == 200:
                uploaded = uploaded + 1
        print("Obras públicas adicionadas: {0}".format(uploaded))


def add_inspections():
    with open("inspections/inspections.csv", "r") as f_in:
        lines = f_in.readlines()
        uploaded = 0
        for line in lines[1:]:
            inspection = line.strip().split(",")
            response = send(BASE_URL + "inspections/add",
                            {
                                "flag": inspection[0],
                                "name": inspection[1],
                                "inquiry_number": inspection[2],
                                "description": inspection[3],
                                "public_work_id": inspection[4],
                                "status": inspection[5],
                                "user_email": inspection[6],
                                "request_date": inspection[7]
                            })
            if response.status_code == 200:
                uploaded = uploaded + 1
        print("Vistorias adicionadas: {0}".format(uploaded))


def add_collects():
    with open("collects/collects.csv", "r") as f_in:
        lines = f_in.readlines()
        uploaded = 0
        for line in lines[1:]:
            collect = line.strip().split(",")
            response = send(BASE_URL + "collects/add",
                            {
                                "id": collect[0],
                                "public_work_id": collect[1],
                                "inspection_flag": collect[2],
                                "queue_status": collect[3],
                                "queue_status_date": collect[4],
                                "date": collect[5],
                                "user_email": collect[6],
                                "comments": collect[7],
                                "public_work_status": collect[8]
                            })
            if response.status_code == 200:
                uploaded = uploaded + 1
        print("Coletas adicionadas: {0}".format(uploaded))


def add_photos():
    with open("photos/photos.csv", "r") as f_in:
        lines = f_in.readlines()
        uploaded = 0
        for line in lines[1:]:
            photo = line.strip().split(",")
            response = send(BASE_URL + "photos/add",
                            {
                                "id": photo[0],
                                "collect_id": photo[1],
                                "type": photo[2],
                                "filepath": photo[3],
                                "latitude": photo[4],
                                "longitude": photo[5],
                                "comment": photo[6],
                                "timestamp": photo[7]
                            })
            # uri_path = str(pathlib.Path(__file__).parent.resolve()) + "/photos/" + photo[3]
            # with open(uri_path, 'rb') as f:
            #     data = f.read()
            # response_media = send(BASE_URL + "images/upload", {"file": uri_path}, files=data)
            
            if response.status_code == 200:
                uploaded = uploaded + 1
        print("Fotos adicionadas: {0}".format(uploaded))


def add_notifications():
    with open("notifications/notifications.csv", "r") as f_in:
        lines = f_in.readlines()
        uploaded = 0
        for line in lines[1:]:
            notification = line.strip().split(",")
            response = send(BASE_URL + "notification/add",
                            {
                                "id": notification[0],
                                "title": notification[1],
                                "inspection_id": notification[2],
                                "content": notification[3],
                                "user_email": notification[4],
                                "answer": notification[5],
                                "timestamp": notification[6]
                            })
            
            if response.status_code == 200:
                uploaded = uploaded + 1
        print("Notificações adicionadas: {0}".format(uploaded))



def add_comments():
    with open("notifications/comments.csv", "r") as f_in:
        lines = f_in.readlines()
        uploaded = 0
        for line in lines[1:]:
            comments = line.strip().split(",")
            response = send(BASE_URL + "notification/add/comments",
                            {
                                "notification_id": comments[0],
                                "content": comments[1],
                                "receive_email": comments[2],
                                "send_email": comments[3],
                                "timestamp": comments[4]
                            })
            
            if response.status_code == 200:
                uploaded = uploaded + 1
        print("Commentários adicionados: {0}".format(uploaded))


def add_users():
    with open("users/users.csv", "r") as f_in:
        lines = f_in.readlines()
        uploaded = 0
        for line in lines[1:]:
            user = line.strip().split(",")
            response = send(BASE_URL + "security/users/create",
                            {
                                "email": user[0],
                                "authentication": user[1],
                                "full_name": user[2],
                                "picture": user[3],
                                "role": user[4]
                            })
            if response.status_code == 200:
                uploaded = uploaded + 1
        print("Usuários adicionados: {0}".format(uploaded))


def add_work_status():
    with open("work_status/status.csv", "r") as f_in:
        lines = f_in.readlines()
        uploaded = 0
        for line in lines[1:]:
            work_status = line.strip().split(",")
            response = send(BASE_URL + "workstatus/add",
                            {"flag": work_status[0],
                             "name": work_status[1],
                             "description": work_status[2]})
            if response.status_code == 200:
                uploaded = uploaded + 1
        print("Estatus de obras adicionados: {0}".format(uploaded))


def add_admin_user():
    response = send(BASE_URL + "security/users/create/admin", {
        "full_name": "Admin Trena",
        "picture": "https://avatars.githubusercontent.com/u/60111910?s=200&v=4",
        "email": "admin@trena.mpmg.mg.br",
        "authentication": "12345678aA"
    })
    if response.status_code == 200:
        print("Usuário admin criado")
    else:
        print("Error when creating admin user")


def update_token() -> bool:
    global USER_TOKEN
    response = requests.post(BASE_URL + "security/users/login",
                             headers={'X-TRENA-KEY': API_KEY},
                             data={'username': 'admin@trena.mpmg.mg.br', 'password': '12345678aA'},
                             verify=False)
    if response.status_code == 200:
        USER_TOKEN = response.json()['access_token']
        print("Token de usuário atualizado")
    return response.status_code == 200


def main():
    add_admin_user()
    if update_token():
        add_users()
        add_municipios("31")
        add_type_works()
        add_type_photos()
        add_work_status()
        add_type_works_work_statuses()
        add_public_work()
        add_inspections()
        add_collects()
        add_photos()
        add_notifications()
        # add_comments()


if __name__ == '__main__':
    main()
