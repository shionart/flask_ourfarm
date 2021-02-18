from controller.UserController import UserController
from config.config import main
from controller.Controller import login_required


@main.route('/')
@login_required
def index():
    """
    docstring
    """
    return UserController().index()

@main.route('/login', methods=['GET', 'POST'])
def login():
    """
    docstring
    """
    return UserController().login()

@main.route('/logout')
@login_required
def logout():
    return UserController().logout()

@main.route('/register', methods=['GET'])
def register():
    """
    docstring
    """
    return UserController().register()



