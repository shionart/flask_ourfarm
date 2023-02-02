from flask.globals import request
from model.Control import Control
from flask.json import jsonify
import requests


class SyncController(object):
    """
    docstring
    """
 

 #sync pindah jadi file sendiri
    def sync_get_control(self):
        """
        Request Get Control main web\n
        Mengambil data control terbaru dari main web.
        """
        url = "https:///bwcr.insightdata.xyz/api/control/"+self.id_user+"/garden"
        devid = {'deviceId': self.id_arduino}
        ambil = requests.get(url, params=devid, headers={
                             'User-Agent': 'Mozilla/5.0'})
        if ambil.status_code==200 :
            print(ambil.status_code)
            data = ambil.json()
            cek = self.read_control() #ngambil current perintah
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

    