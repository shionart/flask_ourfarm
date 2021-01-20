from config.db import connect_db
from repository import insert_to_control, read_control
import requests
class Control:
    """
    Ini kelas control
    """

    def __init__(self, *args):
        """
        Inisiasi control
        """
        if len(args)>1:
            self.id = id
            self.user_id = id
            self.nama = nama
            self.perintah= perintah
            self.status = status
        else:
            self.id = None
            self.user_id = None
            self.nama = None
            self.perintah= None
            self.status = None

    def setId(self, id):
        """
        docstring
        """
        self.id = id
    def setUser_id(self, user_id):
        """
        docstring
        """
        self.user_id = user_id

    def getControl(self):
        url =  "https://bwcr.rizaldiariif.com/public/api/control/"+self.user_id+"/garden"
        devid = {'deviceId':self.id}
        ambil = requests.get(url,params=devid,headers={'User-Agent': 'Mozilla/5.0'})
        data = ambil.json()
        cek = read_control(self.id)
        print(cek)
        if (ambil.status_code == 200 and str(cek['perintah'])!=data["nilai"]) :
            print("data berubah")
            try:
                conn = connect_db()
                cur = conn.cursor()
                cur.execute("UPDATE control SET perintah=%s, status=0 WHERE id_arduino=%s", [ data['nilai'], self.id])
                conn.commit()
            except Exception as e:
                conn.rollback()
                print(e)
            



    