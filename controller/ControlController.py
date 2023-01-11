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

    def page_control(self, id):
        c = self.control
        c.id_arduino =id
        perintah = c.read_control()
        return render_template('control.html', data=perintah)

    def page_list_control(self):
        return render_template('list_control.html')

    def api_list_control(self, id_user):
        """
        mapping hasil query list control per user ke JSON
        """
        c = self.control
        c.id_user=id_user
        list_control = c.read_list_control()
        return jsonify({'list_control': list_control})

    def api_control(self, id):
        c = self.control
        c.id_arduino = id
        if(request.method == "GET"):
            node = c.read_control()
            # Outputnya berupa bundle sensor, data terbaru & kemaren, bardata(Top data)
            if node!=None:
                return node
            else:
                return jsonify({'perintah': '5',
                'status':'0'})
        elif (request.method == "POST"):
            try:
                perintah = str(request.form["perintah"])
                status = str(request.form["status"])
                nama = str(request.form["nama"])
                id_user = str(request.form["id_user"])
                if(request.form["status"] != None or request.form["nama"] != None or request.form["perintah"] != None):
                    c = Control(perintah=perintah, id_arduino=id, status=status, nama=nama, id_user=id_user)
                    c.insert_control()
                else:
                    pass  # skip sek
                return "perintah: {}, status: {}, id: {}, nama:{}".format(perintah, status, id, nama)
            except Exception as e:
                return "error route {}".format(e)
        elif request.method=="DELETE":
            c.id_arduino = str(request.form["id_arduino"])
            c.delete_control()
            return "node {} deleted".format(c.id_arduino)
        
        

    def get_notif(self, id):
        """
        Api untuk ambil data notif
        """
        c = self.control
        c.id_user=id
        return jsonify({"notif": c.read_notified()})