from config.db import connect_db
# from repository import insert_to_control, read_control
import requests
class Control(object):
    """
    Ini kelas control
    """

    def __init__(self, **kwargs):
        """
        Inisiasi Objek Control
        Parameter : id_arduino, id_user, nama, perintah, status
        """
        if len(kwargs)>0:
            self.id_arduino = kwargs.pop("id_arduino", None)
            self.id_user = kwargs.pop("id_user", None)
            self.nama = kwargs.pop("nama", None)
            self.perintah= kwargs.pop("perintah", None)
            self.status = kwargs.pop("status", None)
        else:
            self.id_arduino = None
            self.id_user = None
            self.nama = None
            self.perintah= None
            self.status = None

    def setId_arduino(self, id_arduino):
        """
        docstring
        """
        self.id_arduino = id_arduino
    def getId_arduino(self):
        """
        docstring
        """
        return self.id_arduino
    def setId_user(self, id_user):
        """
        docstring
        """
        self.id_user = id_user
    def getId_user(self):
        """
        docstring
        """
        self.id_arduino
    def setNama(self, nama):
        """
        docstring
        """
        self.nama = nama
    def getNama(self):
        """
        docstring
        """
        return self.nama
    def setPerintah(self, perintah):
        """
        docstring
        """
        self.perintah = perintah
    def getPerintah(self):
        """
        docstring
        """
        return self.perintah
    def setStatus(self, status):
        """
        docstring
        """
        self.status = status
    def getStatus(self):
        """
        docstring
        """
        return self.status

    def read_controls(self):
        """
        Baca udah berapa node yang connect
        """
        conn = connect_db()    
        cur = conn.cursor()
        cur.execute("SELECT * from control")
        nodes = cur.fetchall()
        return nodes

    def read_control(self):
        conn = connect_db()
        cur= conn.cursor()
        cur.execute("SELECT * FROM control WHERE id_arduino=%s",[self.id_arduino])
        data_perintah= cur.fetchone()
        # isi = data_perintah['perintah']
        return data_perintah

    def read_control_id(self):
        conn = connect_db()
        cur= conn.cursor()
        cur.execute("SELECT id_arduino FROM control WHERE id_arduino=%s",[self.id_arduino])
        data_perintah= cur.fetchone()
        # isi = data_perintah['perintah']
        return data_perintah

    def insert_to_control(self):
        """
        Jika belum ada node sebelum nya, maka INSERT
        Bila sudah ada maka UPDATE
        """
        conn=connect_db()
        cur=conn.cursor()
        try:
            # Auto Add Arduino
            cek_control = read_control_id(self.id_arduino)
            if cek_control == None :
                print("Eksekusi insert to control")
                cur.execute("INSERT INTO control (id_arduino, nama, perintah, status) VALUES(%s,%s,%s,%s)",[self.id_arduino,self.nama,"0","1"])
                # Auto Add selesai
            else:
                print("Update control")
                cur.execute("UPDATE control SET perintah=%s, status=%s WHERE id_arduino=%s",[self.perintah,self.status,self.id_arduino])
            conn.commit()
            print("Data control berhasil diupdate!")
        except Exception as error:
            conn.rollback()
            print("gagal update data {}".format(error))
        finally:
            if (conn):
                cur.close()
                conn.close()
                print("MySql ditutup")
        return "selesai"

    def getControl(self):
        """
        Request Get to main web
        """
        url =  "https://bwcr.rizaldiariif.com/public/api/control/"+self.id_user+"/garden"
        devid = {'deviceId':self.id_arduino}
        ambil = requests.get(url,params=devid,headers={'User-Agent': 'Mozilla/5.0'})
        # print(ambil.status_code)
        data = ambil.json()
        cek = self.read_control()
        print("local :"+str(cek['perintah']))
        print("webpusat:"+str(data['nilai']))
        if (ambil.status_code == 200 and str(cek['perintah'])!=data["nilai"]) :
            print("data berubah")
            try:
                conn = connect_db()
                cur = conn.cursor()
                cur.execute("UPDATE control SET perintah=%s, status=0 WHERE id_arduino=%s", [ data['nilai'], self.id_arduino])
                conn.commit()
                cur.close()
                conn.close()
            except Exception as e:
                conn.rollback()
                print(e)

            



    