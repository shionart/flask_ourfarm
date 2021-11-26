from flask.globals import request
from controller.SensorController import SensorController
from controller.ControlController import ControlController
from controller.UserController import UserController
from config.config import main
from controller.Controller import login_required


@main.route('/')
@login_required
def index():
    """
    Route untuk home
    """
    return UserController().index()
#-------------------User---------------------
@main.route('/login', methods=['GET', 'POST'])
def login():
    """
    Route untuk login 
    ------
    methods = get, post
    """
    return UserController().login()

@main.route('/logout')
@login_required
def logout():
    """
    Route untuk logout
    """
    return UserController().logout()

@main.route('/register', methods=['GET'])
def register():
    """
    Route untuk register akun methods = GET
    """
    return UserController().register()
#-----------------User API--------------------------
@main.route('/post_raspi', methods=["POST"])
def post_raspi():
    """
    Route API untuk POST data dari register akun
    """
    return UserController().post_raspi()

# --------Control---------------

@main.route('/dashboard/<id>')
@login_required
def dashboard(id):
    """
    Route untuk dashboard data node <id>
    """
    return ControlController().dashboard(id)

@main.route('/control/<id>')
@login_required
def control(id):
    """
    Route untuk LAMAN control pompa node <id>
    """
    return ControlController().control_page(id)

@main.route('/control')
@login_required
def list_control():
    """
    Route untuk LAMAN list node
    """
    return ControlController().list_control()
#--------------Control API--------------------
@main.route('/get_control/<id>', methods=["GET"])
def get_data_control(id):
    """
    Route API GET untuk semua list arduino dari sebuah user <id>
    """
    return ControlController().get_data_control(id)

@main.route('/api_control/<id>', methods=["GET", "POST"])
def api_data_node(id):
    """
    Route API untuk control hanya pada satu node
    """
    return ControlController().api_data_node(id)

@main.route('/api_queue_control', methods=['GET','POST','DELETE'])
def api_queue_control():
    """
    Route API untuk queue data control
    """
    return ControlController().api_queue_control()
#--------------Notif API-----------------------
@main.route('/api_notif/<id>', methods=['GET', 'POST'])
def api_notif(id):
    """
    Route API untuk get data notif
    """
    if request.method=="GET" :
        # print(request.get_data())
        # print(request.form)
        return ControlController().get_notif(id)
    elif request.method=="POST" :
        # return str(request.form["id_sensor"])
        # SensorController().update_notified(str(request.form["id_sensor"]))
        SensorController().update_notified(id)
        return dashboard(id=id)     

#--------------Sensor API-------------------
@main.route('/input', methods=["POST","DELETE"])
def cud_api_data():
    """
    Route API untuk input data sensor dan Registrasi Node pertama 
    """
    if request.method=="DELETE":
        ControlController().api_data_node("")
    return SensorController().controller_api_data() 
    

@main.route('/get/<id>', methods=["GET"])
def get_data_api(id):
    """
    Route API untuk GET data sensor per Id
    """
    return SensorController().get_data_api(id)


# @main.route('/get_last_updated/<id>', methods=["GET"])
# def get_last_updated(id):
#     """
#     Route API untuk GET data sensor per Id
#     """
#     return SensorController().get_last_updated(id)

