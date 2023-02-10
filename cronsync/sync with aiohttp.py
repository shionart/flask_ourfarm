from MySQLdb import cursors, connect
import requests
import asyncio
import aiohttp 
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

async def post_sensor(session, data):
    """
    docstring
    """

    url = "https://bwcr.insightdata.xyz/api/add/"+str(data['id_user'])+"/garden/"+str(data['id_arduino'])
    perintah = {'lembap': data['kelembapan'],
        'sm':str(data['soil_moist']),
        'suhu':str(data['suhu']),
        'relay':str(data['relay'])
    }
    print("inisiasi get data")
    async with session.get(url, params=perintah, headers={'User-Agent': 'Mozilla/5.0'}) as ambil :
        print(ambil.url)
    # ambil = requests.get(url, params=perintah, headers={
    #                         'User-Agent': 'Mozilla/5.0'})
        status = ambil.status
        if (status == 200):
            print("Successfully posting sensor data"+str(data['id']))
        else:
            print("Failed posting sensor data"+str(data['id'])+" status code"+str(status))
            sensor_not_sent.append(str(data['id']))

async def update_sensor_queued():
    conn = connect(host ='localhost', port =3306 , user= 'root' , passwd='dragonica025', db='db_sister', cursorclass=cursors.DictCursor)
    cur = conn.cursor()
    cur.execute("update sensor set queue=0 where id not in ({})".format(stringed_sensor(sensor_not_sent)) )
    cur.execute("select a.*, b.id_user from sensor a right join control b on a.id_arduino = b.id_arduino where a.queue=1 order by a.time ASC")
    conn.commit()       
    cur.close()
    conn.close()
    pass

async def sync_sensor(session):
    """
    docstring
    """
    list_task=[]
    hasil_query = await read_sensor()
    if len(hasil_query) >0:
        print("Post data sensor Dimulai")
        for data in hasil_query:
            print("membuat task")
            task = asyncio.create_task(post_sensor(session, data))
            list_task.append(task)
        await asyncio.gather(*list_task)
        await update_sensor_queued()
        print("Post data sensor selesai")
    else :
        print("data kosong, tidak ada yg dipost")

async def main() :
    async with aiohttp.ClientSession() as session :
        await sync_sensor(session)

if __name__ == '__main__':
    asyncio.run(main())