from config.db import connect_db
import requests


class Control(object):
    """
    Ini kelas control
    """

    def __init__(self, **kwargs):
        """
        Inisiasi Objek Control
        Parameter : id_arduino, id_user, nama, perintah, status, batas_atas, batas_bawah, jeda
        """
        if len(kwargs) > 0:
            self.id_arduino = kwargs.pop("id_arduino", None)
            self.id_user = kwargs.pop("id_user", None)
            self.nama = kwargs.pop("nama", None)
            self.perintah = kwargs.pop("perintah", None)
            self.status = kwargs.pop("status", None)
            self.batas_atas = kwargs.pop("batas_atas", None)
            self.batas_bawah = kwargs.pop("batas_bawah", None)
            self.jeda = kwargs.pop("jeda", None)
        else:
            self.id_arduino = None
            self.id_user = None
            self.nama = None
            self.perintah = None
            self.status = None
            self.batas_atas = None
            self.batas_bawah = None
            self.jeda = None


    def read_list_control(self):
        """
        Read dari tabel Control berdasarkan user
        """
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT a.id_arduino, a.nama, b.time from control a left join (select c.id_arduino, date_format(max(c.time),'%%a,%%b %%e %%Y %%H:%%i') time from sensor c group by c.id_arduino) b on a.id_arduino=b.id_arduino where a.id_user=%s",[self.id_user])
        list_control = cur.fetchall()
        return list_control

    def read_control(self):
        """
        Read satu baris data dari tabel Control
        """
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM control WHERE id_arduino=%s",
                    [self.id_arduino])
        data_perintah = cur.fetchone()
        # isi = data_perintah['perintah']
        # if data_perintah!=None:
        return data_perintah

    def is_exist_control(self):
        """
        Cek apakah id arduino exist
        """
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT id_arduino FROM control WHERE id_arduino=%s", [
            self.id_arduino])
        data_perintah = cur.fetchone()
        if data_perintah==None:
            return False
        else:
            return True

    def cu_control(self):
        """
        Insert ke tabel Control jika id_arduino non-exist, Update tabel Control jika id_arduino exist
        """
        conn = connect_db()
        cur = conn.cursor()
        try:
            if self.is_exist_control():
                print("Update Control")
                if self.batas_atas!=None:
                    cur.execute("UPDATE control SET perintah=%s, jeda=%s, batas_atas=%s, batas_bawah=%s, status=%s, queue=1 where id_arduino=%s", 
                                [self.perintah, self.jeda,  
                                self.batas_atas, self.batas_bawah, self.status, 
                                self.id_arduino])
                else :
                    cur.execute("UPDATE control SET perintah=%s, status=%s WHERE id_arduino=%s", [
                                self.perintah, self.status, self.id_arduino])
            else:
                print("insert Control")
                cur.execute("INSERT INTO control (id_arduino, id_user, nama, perintah, status) VALUES(%s,%s,%s,%s,%s)", [
                            self.id_arduino, self.id_user, self.nama, "0", "1"])
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

    def delete_control(self):
        """
        Delete dari tabel Control berdasarkan id_arduino
        """
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("DELETE FROM control WHERE id_arduino=%s",[self.id_arduino])
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(e)
        finally :
            if conn:
                cur.close()
                conn.close()         
        
    def read_notified(self):
        """
        Ambil data sensor dari List id_arduino & notif!=0
        """
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("select a.nama, a.id_arduino, date_format(b.time,'%%a, %%b %%e %%Y %%H:%%i') as time, b.soil_moist, b.id as id_sensor, b.notif "+
                        "from control a right join "+ 
                        "(select c.* from sensor c right join (select max(d.time) as timemax from sensor d where d.notif!=0 group by d.id_arduino) e on c.time=e.timemax) b "+
                        "on a.id_arduino=b.id_arduino where a.id_user=%s order by b.time DESC",[self.id_user])
            list_notif = cur.fetchall()
            cur.close()
            conn.close()
            return list_notif
        except Exception as e:
            print(e)

