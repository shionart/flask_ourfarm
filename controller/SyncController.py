from flask.globals import request
from model.Control import Control
from model.QueueControl import QueueControl
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

    def sync_post_control(self):
        """
        Request Post Control to main web\n
        Mengirim data control terbaru dari local ke main web.
        
        """
        cek =self.read_queue_control()
        
        url = "http://bwcr.insightdata.xyz/public/api/control/update/"+self.id_user+"/garden/"+self.id_arduino
        perintah = {'nilai': self.perintah}
        ambil = requests.get(url, params=perintah, headers={
                             'User-Agent': 'Mozilla/5.0'})
        # print(ambil.status_code)
        data = ambil.json()
        cek = self.read_queue_control()
        # print("local :"+str(cek['perintah']))
        # print("webpusat:"+str(data['nilai']))
        if (ambil.status_code == 200 and cek!="KOSONG"):
            print("ada data queue")
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
        else:
            print("Status code : "+ambil.status_code+"queue : "+cek)

    #TODO : buat routing untuk queue control
    def api_queue_control(self):
        """
        Api untuk table queue
        """
        if request.method =="POST":
            id_arduino=str(request.form["id_arduino"])
            id_user=str(request.form["id_user"])
            perintah = int(request.form["perintah"])
            queue = QueueControl(id_arduino=id_arduino, id_user=id_user, perintah=perintah)
            queue.queue_to_control()
            return "Queue control inserted"
        elif request.method == "GET":
            queue = QueueControl()
            read = queue.read_queue_control()
            return jsonify(read) 
        elif request.method == "DELETE":
            idqueue=int(request.form["idqueue_control"])
            if not idqueue:
                queue = QueueControl()
                queue.queue_clear()
            else:
                queue = QueueControl()
                queue.queue_clear_id(idqueue)
            return "queue control cleared"