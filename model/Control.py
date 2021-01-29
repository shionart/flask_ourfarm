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
        cur.execute("SELECT * from control")
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
        

    def getControl(self):
        """
        Request Get to main web
        """
        url = "https://bwcr.rizaldiariif.com/public/api/control/"+self.id_user+"/garden"
        devid = {'deviceId': self.id_arduino}
        ambil = requests.get(url, params=devid, headers={
                             'User-Agent': 'Mozilla/5.0'})
        # print(ambil.status_code)
        data = ambil.json()
        cek = self.read_control()
        print("local :"+str(cek['perintah']))
        print("webpusat:"+str(data['nilai']))
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