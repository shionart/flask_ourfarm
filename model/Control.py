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
        if len(kwargs) > 0:
            self.id_arduino = kwargs.pop("id_arduino", None)
            self.id_user = kwargs.pop("id_user", None)
            self.nama = kwargs.pop("nama", None)
            self.perintah = kwargs.pop("perintah", None)
            self.status = kwargs.pop("status", None)
        else:
            self.id_arduino = None
            self.id_user = None
            self.nama = None
            self.perintah = None
            self.status = None


    def read_controls(self):
        """
        Baca udah berapa node yang connect
        """
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT * from control where id_user=%s",[self.id_user])
        nodes = cur.fetchall()
        return nodes

    def read_control(self):
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM control WHERE id_arduino=%s",
                    [self.id_arduino])
        data_perintah = cur.fetchone()
        # isi = data_perintah['perintah']
        return data_perintah

    def read_control_id(self):
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT id_arduino FROM control WHERE id_arduino=%s", [
            self.id_arduino])
        data_perintah = cur.fetchone()
        # isi = data_perintah['perintah']
        return data_perintah

    def insert_to_control(self):
        """
        Jika belum ada node sebelum nya, maka INSERT
        Bila sudah ada maka UPDATE
        """
        conn = connect_db()
        cur = conn.cursor()
        try:
            # Auto Add Arduino
            cek_control = self.read_control_id()
            if cek_control == None:
                print("Eksekusi insert to control")
                cur.execute("INSERT INTO control (id_arduino, nama, perintah, status) VALUES(%s,%s,%s,%s)", [
                            self.id_arduino, self.nama, "0", "1"])
                # Auto Add selesai
            else:
                print("Update control")
                cur.execute("UPDATE control SET perintah=%s, status=%s WHERE id_arduino=%s", [
                            self.perintah, self.status, self.id_arduino])
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

    def queue_to_control(self):
        """
        untuk stack perubahan control jika response tidak ok
        Obj Control attr : id_arduino, id_user, perintah
        """
        conn=connect_db()
        cur=conn.cursor()
        try:
            cur.execute("INSERT INTO queue_control (id_arduino, id_user, perintah) VALUES(%s,%s,%s)", [
                            self.id_arduino, self.id_user, self.perintah])
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(e)
        finally:
            cur.close()
            conn.close()
    
    def queue_clear(self):
        """
        Clear table queue_control
        """
        conn=connect_db()
        cur=conn.cursor()
        try:
            cur.execute("DELETE FROM queue_control")
            conn.commit()
        except Exception as e :
            print(e)
        finally:
            cur.close()
            conn.close()
    def queue_clear_id(self,idqueue):
        """
        Clear table queue_control
        """
        conn=connect_db()
        cur=conn.cursor()
        try:
            cur.execute("DELETE FROM queue_control where idqueue_control=%s",[idqueue])
            conn.commit()
        except Exception as e :
            print(e)
        finally:
            cur.close()
            conn.close()
        
    def read_queue_control(self):
        """
        Baca control yg ga ke submit
        """
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT * from queue_control where id_arduino=%s",[self.id_arduino])
        nodes = cur.fetchall()
        if not nodes:
            nodes = "KOSONG"
        return nodes

    def getControl(self):
        """
        Request Get Control main web\n
        Mengambil data control terbaru dari main web.
        """
        url = "https://bwcr.rizaldiariif.com/public/api/control/"+self.id_user+"/garden"
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
                try:
                    conn = connect_db()
                    cur = conn.cursor()
                    cur.execute("UPDATE control SET perintah=%s, status=0 WHERE id_arduino=%s", [
                                data['nilai'], self.id_arduino])
                    conn.commit()
                    cur.close()
                    conn.close()
                except Exception as e:
                    conn.rollback()
                    print(e)
        else :
            print("main web cannot be reached")

    def postControl(self):
        """
        Request Post Control to main web\n
        Mengirim data control terbaru dari local ke main web.
        
        """
        cek =self.read_queue_control()
        
        url = "https://bwcr.rizaldiariif.com/public/api/control/update/"+self.id_user+"/garden/"+self.id_arduino
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
            try:
                conn = connect_db()
                cur = conn.cursor()
                cur.execute("UPDATE control SET perintah=%s, status=0 WHERE id_arduino=%s", [
                            data['nilai'], self.id_arduino])
                conn.commit()
                cur.close()
                conn.close()
            except Exception as e:
                conn.rollback()
                print(e)
        else:
            print("Status code : "+ambil.status_code+"queue : "+cek)
    
    def get_notified(self):
        """
        Ambil data sensor dari List id_arduino & notif!=0
        """
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("select a.nama, a.id_arduino, date_format(b.time,'%%a, %%b %%e %%Y %%H:%%i') as time, b.soil_moist, b.id as id_sensor from control a "+
                        "left join ("+
                        "select * from sensor c where c.time in "
                        "(select max(c.time) from sensor c where c.notif=1 group by c.id_arduino)) "+
                        "b on a.id_arduino=b.id_arduino where a.id_user=%s and b.notif=1 order by b.time DESC",[self.id_user])
            list_notif = cur.fetchall()
            cur.close()
            conn.close()
            return list_notif
        except Exception as e:
            print(e)

