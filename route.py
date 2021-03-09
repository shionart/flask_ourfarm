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