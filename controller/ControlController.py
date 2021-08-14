from flask.globals import request
from flask.json import jsonify
from flask.templating import render_template
from model.Control import Control

class ControlController(object):
    """
    Controller dari model Control
    ---
    """
    def __init__(self, **kwargs):
        """
        Control Controller
        --------
        Parameters(sunnah) :
            - id_arduino
            - id_user
            - nama
            - perintah
            - status
        """
        if len(kwargs)>0:
            self.control = Control(
                id_arduino = kwargs.pop("id_arduino", None),
                id_user = kwargs.pop("id_user", None),
                nama = kwargs.pop("nama", None),
                perintah = kwargs.pop("perintah", None),
                status = kwargs.pop("status", None)
            )
        else:
            self.control = Control()

    
    def dashboard(self, id):
        c = self.control
        c.id_arduino =id
        info = c.read_control()
        return render_template('dashboard.html', info=info)

    def control_page(self, id):
        c = self.control
        c.id_arduino =id
        perintah = c.read_control()
        return render_template('control.html', data=perintah)

    def list_control(self):
        return render_template('list_nodes.html')

    def get_data_control(self, id_user):
        c = self.control
        c.id_user=id_user
        nodes = c.read_controls()
        # Outputnya berupa bundle sensor, data terbaru & kemaren, bardata(Top data)
        return jsonify({'nodes': nodes})

    def api_data_node(self, id):
        c = self.control
        c.id_arduino = id
        if(request.method == "GET"):
            node = c.read_control()
            # Outputnya berupa bundle sensor, data terbaru & kemaren, bardata(Top data)
            if node!=None:
                return node
            else:
                return jsonify({'perintah': '5',
                'status':'1'})
        elif (request.method == "POST"):
            try:
                perintah = str(request.form["perintah"])
                status = str(request.form["status"])
                nama = str(request.form["nama"])
                if(request.form["status"] != None or request.form["nama"] != None or request.form["perintah"] != None):
                    c = Control(perintah=perintah, id_arduino=id, status=status, nama=nama)
                    c.insert_to_control()
                else:
                    pass  # skip sek
                return "perintah: {}, status: {}, id: {}, nama:{}".format(perintah, status, id, nama)
            except Exception as e:
                return "error route {}".format(e)

        
        #TODO : buat routing untuk queue control
    def api_queue_control(self):
        """
        Api untuk table queue
        """
        if request.method =="POST":
            id_arduino=str(request.form["id_arduino"])
            id_user=str(request.form["id_user"])
            perintah = int(request.form["perintah"])
            queue = Control(id_arduino=id_arduino, id_user=id_user, perintah=perintah)
            queue.queue_to_control()
            return "Queue control inserted"
        elif request.method == "GET":
            queue = Control()
            read = queue.read_queue_control()
            return jsonify(read) 
        elif request.method == "DELETE":
            idqueue=int(request.form["idqueue_control"])
            if not idqueue:
                queue = Control()
                queue.queue_clear()
            else:
                queue = Control()
                queue.queue_clear_id(idqueue)
            return "queue control cleared"

    def get_notif(self, id):
        """
        Api untuk ambil data notif
        """
        c = self.control
        c.id_user=id
        return jsonify({"notif": c.get_notified()})