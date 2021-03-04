from model.Control import Control
class ControlController(object):
    """
    Controller dari model Control
    ---
    """
    def __init__(self, **kwargs):
        """
        User Controller
        --------
        Parameters(sunnah) :
            - id_arduino
            - id_user
            - nama
            - perintah
            - status
        """
        if len(kwargs)>0:
            self.user = Control(
                id_arduino = kwargs.pop("id_arduino", None),
                id_user = kwargs.pop("id_user", None),
                nama = kwargs.pop("nama", None),
                perintah = kwargs.pop("perintah", None),
                status = kwargs.pop("status", None)
            )
        else:
            self.user = Control()

