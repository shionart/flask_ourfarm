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
    Route untuk register methods = GET
    """
    return UserController().register()

@main.route('/post_raspi', methods=["POST"])
def post_raspi():
    """
    Route API untuk POST data dari register
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
    Route untuk control pompa node <id>
    """
    return ControlController().control_page(id)

@main.route('/control')
@login_required
def list_control():
    """
    Route untuk list node
    """
    return ControlController().list_control()

@main.route('/get_control', methods=["GET"])
def get_data_control():
    """
    Route API untuk control local
    """
    return ControlController().get_data_control()

@main.route('/api_control/<id>', methods=["GET", "POST"])
def api_data_node(id):
    """
    Route API untuk control A node 
    """
    return ControlController().api_data_node(id)

@main.route('/api_queue_control', methods=['GET','POST','DELETE'])
def api_queue_control():
    """
    Route API untuk queue data control
    """
    return ControlController().api_queue_control()

#--------------Sensor-------------------
@main.route('/input', methods=["POST"])
def input_data():
    """
    Route API untuk input data sensor 
    """
    return SensorController().input_data()

@main.route('/get/<id>', methods=["GET"])
def get_data_api(id):
    """
    Route API untuk GET data sensor per Id
    """
    return SensorController().get_data_api(id)


@main.route('/get_last_updated/<id>', methods=["GET"])
def get_last_updated(id):
    """
    Route API untuk GET data sensor per Id
    """
    return SensorController().get_last_updated(id)

