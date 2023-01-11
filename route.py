from flask.globals import request
from controller.SensorController import SensorController
from controller.ControlController import ControlController
from controller.UserController import UserController
from config.config import main
from SessionHandler import login_required



#-------------------HALAMAN---------------------
@main.route('/')
@login_required
def index():
    """
    Route untuk home
    """
    return UserController().index()

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

@main.route('/register', methods=['GET', 'POST'])
def register():
    """
    Route untuk PAGE register 
    """
    return UserController().register()

@main.route('/control')
@login_required
def page_list_control():
    """
    Route untuk LAMAN list node
    """
    return ControlController().page_list_control()

@main.route('/dashboard/<arduinoid>')
@login_required
def dashboard(arduinoid):
    """
    Route untuk dashboard data per <arduinoid>
    """
    return ControlController().dashboard(arduinoid)

@main.route('/control/<arduinoid>')
@login_required
def page_control(arduinoid):
    """
    Route untuk LAMAN control pompa per <id>
    """
    return ControlController().page_control(arduinoid)


#--------------API--------------------
@main.route('/api_list_control/<userid>', methods=["GET"])
def api_list_control(userid):
    """
    Route API GET list Control per userId
    """
    return ControlController().api_list_control(userid)

@main.route('/api_control/<arduinoid>', methods=["GET", "POST"])
def api_control(arduinoid):
    """
    Route API untuk control hanya pada satu node & Registrasi Device
    """
    return ControlController().api_control(arduinoid)

@main.route('/api_queue_control', methods=['GET','POST','DELETE'])
def api_queue_control():
    """
    Route API untuk queue data control
    """
    return ControlController().api_queue_control()

@main.route('/api_notif/<userid>', methods=['GET', 'POST'])
def api_notif(userid):
    """
    Route API untuk get data notif
    """
    if request.method=="GET" :
        return ControlController().get_notif(userid)
    elif request.method=="POST" :
        SensorController().update_notified(request.form['id_arduino'])
        return dashboard(arduinoid=request.form['id_arduino'])     

@main.route('/input', methods=["POST"])
def cud_api_data():
    """
    Route API untuk input data sensor  
    """
    SensorController().controller_api_data() 
    return "success on "+request.method

@main.route('/deleteDevice', methods=["DELETE"])
def delete_api_data():
    """
    Route API untuk delete data sensor & device
    """
    ControlController().api_control("")
    SensorController().controller_api_data() 
    return "success on "+request.method
    

@main.route('/get/<arduinoid>', methods=["GET"])
def api_sensor(arduinoid):
    """
    Route API untuk GET data sensor per Id
    """
    return SensorController().api_sensor(arduinoid)


# @main.route('/get_last_updated/<id>', methods=["GET"])
# def get_last_updated(id):
#     """
#     Route API untuk GET data sensor per Id
#     """
#     return SensorController().get_last_updated(id)

