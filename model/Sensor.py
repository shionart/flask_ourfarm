from config.db import connect_db
import math

class Sensor(object):
    """
    docstring
    """

    def __init__(self, **kwargs):
        """
        docstring
        """
        if len(kwargs)>0:
            self.id = kwargs.pop("id_sensor", None)
            self.time = kwargs.pop("time", None)
            self.suhu =  kwargs.pop("suhu", None)
            self.kelembapan = kwargs.pop("kelembapan", None)
            self.soil_moist = kwargs.pop("soil_moist", None)
            self.relay = kwargs.pop("relay", None)
            self.id_arduino = kwargs.pop("id_arduino", None)
        else:
            self.id = None
            self.time = None
            self.suhu =  None
            self.kelembapan = None
            self.soil_moist = None
            self.relay = None
            self.id_arduino = None
            

        
    
   # def __init__(self, id, time, suhu, kelembapan, soil_moist, relay, id_arduino):
        """
        constructor
        """
        # self.id = id
        # self.time = time
        # self.suhu =  suhu
        # self.kelembapan = kelembapan
        # self.soil_moist = soil_moist
        # self.relay = relay
        # self.id_arduino = id_arduino
        
    
    def printSensor(self):
        """
        docstring
        """
        print("Ini fungsi class sensor")

    def setId_arduino(self, id_arduino):
        """
        docstring
        """
        self.id_arduino = id_arduino
    
    # def insert_to_sensor(self):
    #     conn = connect_db()
    #     baca_suhu=self.suhu
    #     baca_lembap=self.lembap
    #     try:
    #         if math.isnan(baca_suhu) or math.isnan(baca_lembap) :
    #             suhu=100
    #             lembap=100
    #         cursor = conn.cursor()
    #         query = "INSERT INTO sensor (suhu, kelembapan, soil_moist, relay, id_arduino) VALUES (%s, %s, %s, %s, %s)"
    #         tuple = (self.suhu, self.lembap, self.soil_moist, self.relay, self.id_arduino)
    #         try:
    #             print("Eksekusi insert to table")
    #             cursor.execute("INSERT INTO sensor (suhu, kelembapan, soil_moist, relay, id_arduino) VALUES (%s, %s, %s, %s, %s)",[suhu, lembap, sm, rel, id_arduino])
    #             conn.commit()
    #         except Exception as error:
    #             print("error {}".format(error))
    #             conn.rollback()
    #         print("Data berhasil dimasukkan")
    #         print("Data DHT: {}, {}, data sm: {}, data id_arduino:{}".format(baca_suhu,baca_lembap,sm,id_arduino))
    #     except Exception as error:
    #         print("Gagal memasukkan data {}".format(error))
    #     finally:
    #         if (conn):
    #             cursor.close()
    #             conn.close()
    #             print("MySql ditutup")
    #     return "selesai"

# -----baca tabel Sensor-----
    def read_sensor_class(self):
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM sensor WHERE id_arduino=%s ORDER BY time DESC",[self.id_arduino])
        data = cur.fetchone()
        print(data)

