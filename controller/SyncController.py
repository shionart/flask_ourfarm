from flask.globals import request
from model.Control import Control
from model.Sensor import Sensor
from flask.json import jsonify
import requests

from model.Sensor import Sensor


class SyncController(object):
    """
    docstring
    """
 

 #sync pindah jadi file sendiri
    def read_control(self, id_arduino, id_user):
        """
        Request Get Control main web\n
        Mengambil data control terbaru dari main web.
        """

        url = "https:///bwcr.insightdata.xyz/api/control/"+id_user+"/garden"
        devid = {'deviceId': id_arduino}
        ambil = requests.get(url, params=devid, headers={
                             'User-Agent': 'Mozilla/5.0'})
        if ambil.status_code==200 :
            print(ambil.status_code)
            data = ambil.json()
            cek = Control().read_control() #ngambil current perintah
            print("local :"+str(cek['perintah']))
            print("webpusat:"+str(data['nilai']))
            # if not cek :
            #     print("Table Control Kosong!")
            # else :
            if (ambil.status_code == 200 and str(cek['perintah']) != data["nilai"]):
                print("data berubah")
                control = Control(id_arduino=self )
                control.cu_control()
                # try:
                #     conn = connect_db()
                #     cur = conn.cursor()
                #     cur.execute("UPDATE control SET perintah=%s, status=0 WHERE id_arduino=%s", [
                #                 data['nilai'], self.id_arduino])
                #     conn.commit()
                #     cur.close()
                #     conn.close()
                # except Exception as e:
                #     conn.rollback()
                #     print(e)
        else :
            print("main web cannot be reached")
    

    def upload_control(self, id_arduino, id_user, nilai):
        """
        Request Get Control main web\n
        Mengambil data control terbaru dari main web.
        """

        url = "https://bwcr.insightdata.xyz/api/control/update/"+id_user+"/garden/"+id_arduino
        devid = {'nilai': nilai}
        ambil = requests.get(url, params=devid, headers={
                             'User-Agent': 'Mozilla/5.0'})
        if ambil.status_code==200 :
            print(ambil.status_code)
            data = ambil.json()
            cek = Control().read_control() #ngambil current perintah
            print("local :"+str(cek['perintah']))
            print("webpusat:"+str(data['nilai']))
            # if not cek :
            #     print("Table Control Kosong!")
            # else :
            if (ambil.status_code == 200 and str(cek['perintah']) != data["nilai"]):
                print("data berubah")
                control = Control(id_arduino=self )
                control.cu_control()
                # try:
                #     conn = connect_db()
                #     cur = conn.cursor()
                #     cur.execute("UPDATE control SET perintah=%s, status=0 WHERE id_arduino=%s", [
                #                 data['nilai'], self.id_arduino])
                #     conn.commit()
                #     cur.close()
                #     conn.close()
                # except Exception as e:
                #     conn.rollback()
                #     print(e)
        else :
            print("main web cannot be reached")

    def upload_data_sensor(self, id_arduino):
        """
        docstring
        """
        c = Sensor(id_arduino=id_arduino).read_queued()
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
                Sensor(id_sensor=str(data['id'])).update_queued()
            else:
                print("Failed posting sensor data"+str(data['id'])+" status code"+str(ambil.status_code))
        return "Post to web pusat done"

    