#functions
import requests
import Config
import Text
import sqlite3

async def payment_info(orderId):
    url_orders = 'https://pay-test.raif.ru/api/payment/v1/orders/' + orderId
    response_order = await response(url_orders, orderId, orderId, Config.headers)
    if response_order.status_code == 200:
        all_keys = dict(response_order.json())
        if 'qr' not in all_keys:
            return Text.qr_code   
        qrId = response_order.json()['qr']['id']
        url_payment_info = 'https://pay-test.raif.ru/api/sbp/v1/qr/'+ response_order.json()['qr']['id'] +'/payment-info'
        response_qr = await response(url_payment_info, qrId, qrId, Config.headers)
        paymentStatus = response_qr.json()['paymentStatus']
        return paymentStatus
    else:
        return Text.orderr_not_find

async def response(url, param_name, param_value, headers):
    params = dict(param_name = param_value)
    request = requests.get(url, params=params, headers=headers)
    return request

async def convert(result):   
    return Text.status_orderr.get(result, Text.orderr_not_find)

async def create_db(name):
        conn = sqlite3.connect('ashash.db')
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS Admins (idAdminTable INTEGER PRIMARY KEY autoincrement, idAdmin varchar(100))')
        cursor.execute('CREATE TABLE IF NOT EXISTS Chats (idChatTable INTEGER PRIMARY KEY autoincrement, idChat int)')
        cursor.execute('''INSERT INTO Admins (idAdmin) VALUES (?)''', (name,))
        cursor.execute('''INSERT INTO Chats (idChat) VALUES (?)''', (-1002079077669,))
        conn.commit()
        conn.close()

async def askpass(password):
    if password.text == Config.password:
        await create_db(password.from_user.username) 

async def insert_admin(admins):
    conn = sqlite3.connect('ashash.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO Admins (idAdmin) VALUES (?)''', (admins,))
    conn.commit()
    conn.close()
 
async def insertAdmins(admins):
    conn = sqlite3.connect('ashash.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Admins WHERE idAdmin = ?", (admins,))
    existing_admin = cursor.fetchone()
    conn.close()
    if existing_admin is None:
        await insert_admin(admins)
        return True
    else:
        return False

async def delete_admin(admin_id):
    conn = sqlite3.connect('ashash.db')
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM Admins WHERE idAdmin = ?''', (admin_id,))
    conn.commit()
    conn.close()
 
async def deleteAdmins(admins):
    conn = sqlite3.connect('ashash.db')
    cursor = conn.cursor()
    desired_admin=None
    adm_count = await getAdm()
    if len(adm_count)!=1:
        cursor.execute("SELECT * FROM Admins WHERE idAdmin = ?", (admins,))
        desired_admin = cursor.fetchone()
        conn.close()
    if desired_admin is not None:
        await delete_admin(desired_admin[1])
        return True
    else:
        return False

async def insert_chat(idchat):
    conn = sqlite3.connect('ashash.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO Chats (idChat) VALUES (?)''', (idchat,))
    conn.commit()
    conn.close()

async def insertChat(idchat):
    conn = sqlite3.connect('ashash.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Chats WHERE idChat = ?", (idchat,))
    existing_chat = cursor.fetchone()
    conn.close()
    if existing_chat is None:
        await insert_chat(idchat)
        return True
    else:
        return False

async def delete_chat(idchat):
    conn = sqlite3.connect('ashash.db')
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM Chats WHERE idChat = ?''', (idchat,))
    conn.commit()
    conn.close()

async def deleteChats(idchat):
    conn = sqlite3.connect('ashash.db')
    cursor = conn.cursor()
    desired_chat=None
    cursor.execute("SELECT * FROM Chats WHERE idChat = ?", (idchat,))
    desired_chat = cursor.fetchone()
    conn.close()
    if desired_chat is not None:
        await delete_chat(desired_chat[1])
        return True
    else:
        return False

async def getAdm():
    conn = sqlite3.connect('ashash.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Admins")
    adm = cursor.fetchall()
    adm = [row[1] for row in adm]
    return adm

async def ShowAdmins():
    adm = await getAdm()
    text = '\n'.join(f"{index + 1}. {item}" for index, item in enumerate(adm))
    return text

async def getCht():
    conn = sqlite3.connect('ashash.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Chats")
    cht = cursor.fetchall()
    cht = [row[1] for row in cht]
    return cht

async def ShowChats():
        cht = await getCht()
        if len(cht) != 0:
            text = '\n'.join(f"{index + 1}. https://web.telegram.org/a/#{item}" for index, item in enumerate(cht))
            return text
        else:
            text = Text.no_work_chats
            return text