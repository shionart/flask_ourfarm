from MySQLdb import cursors, connect
import requests
import asyncio

sensor_not_sent = []


def stringed_sensor(a):
    """
    docstring
    """
    result = "0"
    for b in a:
        result+=" ,"+b
    return result

async def read_sensor():
    conn = connect(host ='localhost', port =3306 , user= 'root' , passwd='dragonica025', db='db_sister', cursorclass=cursors.DictCursor)
    cur = conn.cursor()
    cur.execute("select a.*, b.id_user from sensor a right join control b on a.id_arduino = b.id_arduino where a.queue=1 order by a.time ASC limit 50")
    c = cur.fetchall()
    cur.close()
    conn.close()
    return c

async def post_sensor(data):
    """
    docstring
    """
    url = "https://bwcr.insightdata.xyz/api/add/"+str(data['id_user'])+"/garden/"+str(data['id_arduino'])
    perintah = {'lembap': data['kelembapan'],
        'sm':data['soil_moist'],
        'suhu':data['suhu'],
        'relay':data['relay']
    }
    print("inisiasi post data sensor id :"+str(data['id']))
    ambil = requests.get(url, params=perintah, headers={
                            'User-Agent': 'Mozilla/5.0'})
    print(ambil.url)
    if (ambil.status_code == 200):
        print("Successfully posting sensor data"+str(data['id']))
    else:
        print("Failed posting sensor data"+str(data['id'])+" status code"+str(ambil.status_code))
        sensor_not_sent.append(str(data['id']))

async def update_sensor_queued():
    try:
        print("inisiasi update table queued")
        conn = connect(host ='localhost', port =3306 , user= 'root' , passwd='dragonica025', db='db_sister', cursorclass=cursors.DictCursor)
        cur = conn.cursor()
        cur.execute("update sensor set queue=0 where id not in ({})".format(stringed_sensor(sensor_not_sent)) )
        conn.commit()       
        cur.close()
        conn.close()
    except Exception as e:
        print(e)
    print("update selesai")

async def sync_sensor():
    """
    docstring
    """
    list_task=[]
    hasil_query = await read_sensor()
    if len(hasil_query) >0:
        print("Post data sensor Dimulai")
        for data in hasil_query:
            print("Membuat task sensor :"+str(data['id']))
            task = asyncio.create_task(post_sensor(data))
            list_task.append(task)
        await asyncio.gather(*list_task)
        await update_sensor_queued()
        print("Post data sensor selesai")
    else :
        print("data kosong, tidak ada yg dipost")

async def main() :
    await sync_sensor()

if __name__ == '__main__':
    asyncio.run(main())