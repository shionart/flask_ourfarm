
from flask.globals import request
from flask.json import jsonify
from model.Sensor import Sensor


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
    
    def input_data(self):
        self.sensor = Sensor(suhu = 0.0, 
            kelembapan = 0.0,
            soil_moist = 0.0,
            relay = 0,
            id_arduino = 0)
        s= self.sensor
    # perintah arduino
        try:
            if request.method == "POST":
                s.suhu = float(request.form["suhu"])
                s.kelembapan = float(request.form["lembap"])
                s.soil_moist= float(request.form["sm"])
                s.relay = int(request.form["relay"])
                s.id_arduino = str(request.form["id_arduino"])
                s.insert_to_sensor()
                return "suhu : {}, kelembapan : {}, soil moisture : {}, relay : {}, id : {}".format(s.suhu, s.kelembapan, s.soil_moist, s.relay, s.id_arduino)
        except Exception as e:
            return "error {}".format(e)

    
    def get_data_api(self, id):
        self.sensor = Sensor(id_arduino=id)
        s = self.sensor
        sensor, curr_data, bar_data = s.read_sensor()
        yesterday = s.read_yesterday()
        # Outputnya berupa bundle sensor, data terbaru & kemaren, bardata(Top data)
        return jsonify({'sensor': sensor, 'curr_data': curr_data, 'bar_data': bar_data, 'yesterday': yesterday})