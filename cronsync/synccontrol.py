from datetime import datetime
from MySQLdb import cursors, connect
import requests
import asyncio


async def read_control():
    conn = connect(host ='localhost', port =3306 , user= 'root' , passwd='dragonica025', db='db_sister', cursorclass=cursors.DictCursor)
    cur = conn.cursor()
    cur.execute("select * from control")
    c = cur.fetchall()
    cur.close()
    conn.close()
    return c

async def get_control(data):
    """
    docstring
    """
    url = "https://bwcr.insightdata.xyz/api/control/"+str(data['id_user'])+"/garden"
    param = {'deviceId': str(data['id_arduino'])
    }
    print("inisiasi get data control id :"+str(data['id_arduino']))
    ambil = requests.get(url, params=param, headers={
                            'User-Agent': 'Mozilla/5.0'})
    print(ambil.url)
    if (ambil.status_code == 200):
        print("Successfully get control data"+str(data['id_arduino']))
        print(ambil.json())
        hasil_json = ambil.json()
        pusat_timestamp = datetime.strptime(hasil_json['timestamp'], '%d-%m-%y %H:%M:%S')
        print(str(pusat_timestamp)+"  "+str(data['timestamp']))
        if pusat_timestamp > data['timestamp']:
            print("Perbarui perintah")
            await update_control(hasil_json['nilai'], data['id_arduino'])
        else:
            print("diemin bae")
    else:
        print("Failed get control data"+str(data['id_arduino'])+" status code"+str(ambil.status_code))
        # return ""

async def update_control(perintah, id_arduino):
    try:
        print("inisiasi update table control")
        conn = connect(host ='localhost', port =3306 , user= 'root' , passwd='dragonica025', db='db_sister', cursorclass=cursors.DictCursor)
        cur = conn.cursor()
        cur.execute("update control set perintah=%s where id_arduino=%s", [perintah, id_arduino] )
        conn.commit()       
        cur.close()
        conn.close()
    except Exception as e:
        print(e)
    print("update selesai")

async def sync_control():
    """
    docstring
    """
    list_task=[]
    hasil_query = await read_control()
    if len(hasil_query) >0:
        print("Get control data Dimulai")
        for data in hasil_query:
            print("Membuat task control :"+str(data['id_arduino']))
            task = asyncio.create_task(get_control(data))
            list_task.append(task)
        await asyncio.gather(*list_task)
        print("Post data control selesai")
    else :
        print("data kosong, tidak ada yg dipost")

async def main() :
    await sync_control()

if __name__ == '__main__':
    asyncio.run(main())