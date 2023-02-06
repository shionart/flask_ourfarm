from statistics import mean
from config.db import connect_db
from datetime import date
import math

class Sensor(object):
    """
    Class for Table Sensor \n
    --------
    Attribute / column : 
        - id 
        - time
        - suhu
        - kelembapan
        - soil_moist
        - relay
        - id_arduino
    -------
    Function :
        - insert_to_sensor()
        - read_sensor()
        - read_yesterday()
        - mean_yesterday(sensors)
    """

    def __init__(self, **kwargs):
        """
        Constructor Sensor \n
        Parameters : id, time, suhu, kelembapan, soil_moist, relay, id_arduino
        -------
        Function :
            - cu_control()
            - read_sensor()
            - read_yesterday()
            - mean_yesterday(sensors)
        """
        if len(kwargs)>0:
            self.id_sensor = kwargs.pop("id_sensor", None)
            self.time = kwargs.pop("time", None)
            self.suhu =  kwargs.pop("suhu", None)
            self.kelembapan = kwargs.pop("kelembapan", None)
            self.soil_moist = kwargs.pop("soil_moist", None)
            self.relay = kwargs.pop("relay", None)
            self.id_arduino = kwargs.pop("id_arduino", None)
            self.notif = kwargs.pop("notif", None)
        else:
            self.id_sensor = None
            self.time = None
            self.suhu =  None
            self.kelembapan = None
            self.soil_moist = None
            self.relay = None
            self.id_arduino = None
            self.notif = None
    
    def insert_to_sensor(self):
        """
        Memasukkan data ke table sensor.
        Memberi flag pada data berdasarkan nilai dari sensor yang masuk, 
        """
        conn = connect_db()
        baca_suhu=self.suhu
        baca_lembap=self.kelembapan
        try:
            if math.isnan(baca_suhu) or math.isnan(baca_lembap) :
                self.suhu=0
                self.kelembapan=0
            cursor = conn.cursor()
            query = "INSERT INTO sensor (suhu, kelembapan, soil_moist, relay, id_arduino, notif) VALUES (%s, %s, %s, %s, %s, %s)"
            isituple = (self.suhu, self.kelembapan, self.soil_moist, self.relay, self.id_arduino, self.notif)
            try:
                print("Eksekusi insert to table")
                cursor.execute(query,isituple)
                conn.commit()
            except Exception as error:
                print("error {}".format(error))
                conn.rollback()
            print("Data berhasil dimasukkan")
        except Exception as error:
            print("Gagal memasukkan data {}".format(error))
        finally:
            if (conn):
                cursor.close()
                conn.close()
                print("MySql ditutup")
        return "selesai"

    def delete_sensor_arduino(self):
        """
        Fungsi menghapus semua data sensor per Id_arduino
        """
        conn = connect_db()
        try:
            cur = conn.cursor()
            query = "DELETE FROM sensor WHERE id_arduino=%s "
            cur.execute(query,(self.id_arduino, ))
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(e)
        finally:
            if (conn):
                cur.close()
                conn.close()

    def read_sensor(self):
        """
        Membaca Table Sensor\n
        Tanpa parameter
        """
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM sensor WHERE id_arduino=%s ORDER BY time DESC LIMIT 1000",[self.id_arduino])
        data = cur.fetchall()
        cur.close()
        conn.close()
        if data :
            sensor = self.get_sensor(data)
            top_data = self.read_top(sensor)
            curr_data = sensor[0]
            return sensor, curr_data, top_data
        else :
            return None, None, None


    #TODO pindahin ke service
    def get_sensor(self,data):
        """
        Parsing data table sensor -> json
        """
        li = []
        for dat in data:
            di = {}
            waktu = dat['time']
            tanggal = waktu.strftime("%Y/%m/%d")
            jam = waktu.strftime("%H:%M:%S")
            di['tanggal'] = tanggal
            di['jam'] = jam
            di['suhu'] = dat['suhu']
            di['lembap'] = dat['kelembapan']
            di['sm'] = dat['soil_moist']
            di['relay'] = dat['relay']
            di['id']=dat['id']
            li.append(di)
        return li
    #TODO pindahin ke service
    def read_top(self, data):
        """
        Mengambil 10 data terakhir
        """
        top = data[:10]
        top = top[::-1]
        ret = {}
        li_suhu = []
        li_lembap = []
        li_sm = []
        li_relay = []
        li_cahaya = []
        for i in top:
            li_suhu.append(i['suhu'])
            li_lembap.append(i['lembap'])
            li_sm.append(i['sm'])
            li_relay.append(i['relay'])
            ret = {
                'suhu':li_suhu,
                'lembap':li_lembap,
                'sm':li_sm,
                'relay':li_relay
                }
        return ret
    
    def read_yesterday(self):
        """
        Mengambil rerata data 3 hari terakhir \n
        Dan membandingkannya dengan data hari ini
        """
        conn = connect_db()
        cur = conn.cursor()
        #ini tambahan\
        try:
            cur.execute("SELECT * FROM sensor WHERE DATE(time) >= DATE(NOW() - INTERVAL 3 DAY) AND id_arduino=%s order by id desc",[self.id_arduino])
            data = cur.fetchall()
            sensor = self.get_sensor(data)
            y_suhu, y_lembap, y_sm = self.mean_yesterday(sensor)
        except Exception as e:
            y_suhu = 0
            y_lembap = 0
            y_sm = 0
        #tambah end
        sensor,curr_data,bar = self.read_sensor()
        #tambahan - edit
        if y_suhu != 0:
            suhu_yes=(curr_data['suhu']-y_suhu)
        else:
            suhu_yes = 0
        if y_lembap != 0:
            lembap_yes=(curr_data['lembap']-y_lembap)
        else:
            lembap_yes = 0
        if y_sm != 0:
            sm_yes = (curr_data['sm']-y_sm)
        else:
            sm_yes = 0
        # tambah -edit end
        sign = lambda x: (1, 0)[x <= 0]
        yesterday = dict()
        yesterday['suhu'] = {'nilai':float(round(suhu_yes,2)),'sign':sign(suhu_yes)}
        yesterday['lembap'] = {'nilai':float(round(lembap_yes,2)), 'sign':sign(lembap_yes)}
        yesterday['sm'] = {'nilai':float(round(sm_yes,2)), 'sign':sign(sm_yes)}
        #return jsonify({'suhu':suhu_yes,'lembap':lembap_yes,'sm':sm_yes})
        cur.close()
        conn.close()
        return yesterday
    
    def mean_yesterday(self, sensors):
        """
        Rerata dari data sensor yang dimasukkan
        """
        list_suhu = []
        list_lembap = []
        list_sm = []
        for sensor in sensors:
            list_suhu.append(sensor['suhu'])
            list_lembap.append(sensor['lembap'])
            list_sm.append(sensor['sm'])
        mean_suhu = mean(list_suhu)
        mean_lembap = mean(list_lembap)
        mean_sm = mean(list_sm)
        return mean_suhu,mean_lembap,mean_sm


    # def last_updated(self):
    #     """
    #     Ambil tanggal terakhir data terupdate
    #     """
    #     conn = connect_db()
    #     cur = conn.cursor()
    #     cur.execute("SELECT time FROM sensor WHERE id_arduino=%s order by time DESC limit 1",[self.id_arduino])
    #     last_date = cur.fetchone()
    #     last_date=last_date['time'].strftime("%d/%m/%Y")
    #     currDate = date.today().strftime("%d/%m/%Y")
    #     if last_date==currDate:
    #         last_date="Hari ini"
    #     cur.close()
    #     conn.close()
    #     return last_date

    def update_notified(self):
        """
        Update notif jadi read per id_arduino
        """
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("UPDATE sensor SET notif=0 WHERE id_arduino=%s and time<=now() and notif!=0", [self.id_arduino])
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            conn.rollback()
            print(e)

    def read_queued(self):
        """
        Read queued data sensor
        """
        conn=connect_db()
        cur = conn.cursor()
        cur.execute("select a.*, b.id_user from sensor a right join control b on a.id_arduino = b.id_arduino where a.queue=1 and a.id_arduino=%s order by a.time ASC", [self.id_arduino])
        c = cur.fetchall()
        return c
    
    def update_queued(self):
        """
        Update queue jadi queued per id_arduino
        """
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("update sensor set queue=0 where id=%s", [self.id_sensor])
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            conn.rollback()
            print(e)