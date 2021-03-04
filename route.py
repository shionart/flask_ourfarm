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
    Route untuk POST data dari register
    """
    return UserController().post_raspi()



