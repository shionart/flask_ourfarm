from MySQLdb import cursors, connect
import requests

def test():

    conn = connect(host ='localhost', port =3306 , user= 'root' , passwd='dragonica025', db='db_sister', cursorclass=cursors.DictCursor)
    cur = conn.cursor()
    cur.execute("select a.*, b.id_user from sensor a right join control b on a.id_arduino = b.id_arduino where a.queue=1 order by a.time ASC")
    c = cur.fetchall()
    for data in c:
        url = "https://bwcr.insightdata.xyz/api/add/"+str(data['id_user'])+"/garden/"+str(data['id_arduino'])
        perintah = {'lembap': data['kelembapan'],
            'sm':data['soil_moist'],
            'suhu':data['suhu'],
            'relay':data['relay']
        }
        ambil = requests.get(url, params=perintah, headers={
                                'User-Agent': 'Mozilla/5.0'})
        print(ambil.url)
        if (ambil.status_code == 200):
            print("Successfully posting sensor data"+str(data['id']))
            cur.execute("update sensor set queue=0 where id=%s", [data['id']])
        else:
            print("Failed posting sensor data"+str(data['id'])+" status code"+str(ambil.status_code))
    conn.commit()       
    cur.close()
    conn.close()
    return "okeee"

test()
