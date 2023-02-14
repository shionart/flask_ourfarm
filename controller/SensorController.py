
from flask.globals import request
from flask.json import jsonify
from model.Sensor import Sensor, math
from model.Control import Control



class SensorController(object):
    """
    Controller dari model Sensor
    """
    
    def __init__(self, **kwargs):
        """
        Sensor Controller
        --------
        Parameters(sunnah) :
            - id 
            - time
            - suhu
            - kelembapan
            - soil_moist
            - relay
            - id_arduino
        """
        if len(kwargs)>0:
            self.sensor = Sensor(
                id = kwargs.pop("id_sensor", None),
                time = kwargs.pop("time", None),
                suhu =  kwargs.pop("suhu", None),
                kelembapan = kwargs.pop("kelembapan", None),
                soil_moist = kwargs.pop("soil_moist", None),
                relay = kwargs.pop("relay", None),
                id_arduino = kwargs.pop("id_arduino", None)
            )
        else:
            self.sensor = Sensor()
    
    def controller_api_data(self):
        """
        controller cud api data sensor arduino
        """
        self.sensor = Sensor(suhu = 0.0, 
            kelembapan = 0.0,
            soil_moist = 0.0,
            relay = 0,
            id_arduino = 0,
            notif=0)
        s= self.sensor
    # perintah arduino
        try:
            if request.method == "POST":
                s.suhu = float(request.form["suhu"])
                s.kelembapan = float(request.form["lembap"])
                s.soil_moist= float(request.form["sm"])
                s.relay = int(request.form["relay"])
                s.id_arduino = str(request.form["id_arduino"])
                c = Control(id_arduino=s.id_arduino).read_control()
                # Ini dikommen dulu karena 1-2 detik hanya untuk sent request nya
                if math.isnan(s.kelembapan) or math.isnan(s.suhu) :
                    s.notif=4
                elif s.soil_moist>c['batas_atas']:
                    s.notif=2
                elif s.soil_moist<c['batas_bawah']:#to do parameter benchmark kelembapan dijadiin variable
                    s.notif=1
                elif s.relay==1 and c['perintah']==1:
                    s.notif=3
                s.insert_to_sensor()
                return "suhu : {}, kelembapan : {}, soil moisture : {}, relay : {}, id : {}".format(s.suhu, s.kelembapan, s.soil_moist, s.relay, s.id_arduino)
            elif request.method=="DELETE" :
                s.id_arduino = str(request.form["id_arduino"])
                s.delete_sensor_arduino()
                return "data {} deleted".format(s.id_arduino)
        except Exception as e:
            return "error {}".format(e)

    
    def api_sensor(self, id):
        self.sensor = Sensor(id_arduino=id)
        s = self.sensor
        sensor, curr_data, bar_data = s.read_sensor()
        if sensor is not None :
            yesterday = s.read_yesterday()
            # Outputnya berupa bundle sensor, data terbaru & kemaren, bardata(Top data)
            return jsonify({'sensor': sensor, 'curr_data': curr_data, 'bar_data': bar_data, 'yesterday': yesterday})
        else:
            return jsonify({'sensor': {}, 'curr_data': {}, 'bar_data': {}, 'yesterday': {}})

    # def get_last_updated(self, id):
    #     """
    #     Controller untuk get last update from certain arduino
    #     """
    #     self.sensor = Sensor(id_arduino=id)
    #     s = self.sensor
    #     last_date = s.last_updated()
    #     return jsonify({'time':last_date})
    
    def update_notified(self, id):
        """
        Controller untuk update notif pada data sensor
        """
        self.sensor = Sensor(id_arduino=id)
        s = self.sensor
        s.update_notified()
        print("Notif has been read {}".format(s.id_arduino))