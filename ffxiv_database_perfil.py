from pickle import NONE
from urllib import request
import requests
import json
import sqlite3

def addicionar_database():
    player_input = input("Type the character First and Last name: ")
    server_input = input("Type the character server: ").lower()

    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor_select = conn.cursor()

    request_get = json.loads(requests.get(f'https://xivapi.com/character/search?name={player_input}&server={server_input}').content)
    lodestone_id = request_get["Results"][0]["ID"]
    request_fc = json.loads(requests.get(f'https://xivapi.com/character/{lodestone_id}?data=FC,FCM').content)
    fc_members_info = request_fc["FreeCompanyMembers"]

    for membro in fc_members_info:
        cursor_select.execute(f"""
        SELECT COUNT(*) FROM Usuarios WHERE lodestone_id = '{membro['ID']}';
        """)
        count = cursor_select.fetchone()[0]
        if count == 0:
            cursor.execute(f"""
            INSERT INTO Usuarios (lodestone_id, name, free_company, server)
            VALUES ('{membro["ID"]}', '{membro["Name"]}', '{request_fc["FreeCompany"]["Name"]}', '{membro["Server"]}')
            """)
    conn.commit()

    print('Dados inseridos com sucesso.')

    conn.close()

def calcular_porcent(valor, valor_max):
    return (valor*100)/valor_max


def detalhar_personagem():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor_select = conn.cursor()
    
    cursor.execute("""
    SELECT id, name  FROM Usuarios;
    """)

    for linha in cursor.fetchall():
        print(f'{linha[0]} - {linha[1]}')
    
    personagem_select = int(input('\nType the character number that you want to consult: '))
    print(personagem_select)
    cursor_select.execute(f"""
    SELECT lodestone_id FROM Usuarios WHERE id = {personagem_select};
    """)
    item = int(cursor_select.fetchone()[0])
    request_char_info = json.loads(requests.get(f'https://xivapi.com/character/{item}?data=FC,MIMO').content)
    minion_porcent = calcular_porcent(len(request_char_info["Minions"]), 450)
    mount_porcent = calcular_porcent(len(request_char_info["Mounts"]), 230)
    print(f"""\nCharacter: {request_char_info["Character"]["Name"]}
Server: {request_char_info["Character"]["Server"]}
Free Company: {request_char_info["Character"]["FreeCompanyName"]}
Minions: {len(request_char_info["Minions"])} ({round(minion_porcent, 2)}% obtain)
Mounts: {len(request_char_info["Mounts"])} ({round(mount_porcent, 2)}% obtain)   """)

    conn.close()


def main():
    escolher_funcao = int(input("""Choose one Option:
1 - Add character to database. 
2 - Detail registered character.

"""))
    if escolher_funcao == 1:
        addicionar_database()
        return
    elif escolher_funcao == 2:
        detalhar_personagem()
        return
    else:
        print('\nOption not available,please start over.\n')
        main()


main()